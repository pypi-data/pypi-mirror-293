from __future__ import annotations
from tqdm.auto import tqdm
from typing import Sequence, Optional, NamedTuple, cast
import torch
from torch import Tensor


def initialize_cluster_centers(V: Sequence[Tensor]) -> Tensor:
    # In all generality, inputs can be a sequence of point clouds of varying lengths.
    # We set K as the 50% of the median cardinality of the views
    K = int(0.5 * torch.tensor([p.shape[1] for p in V]).median())
    # To initialize cluster centers, we sample the unit sphere,
    # by randomly selecting azimuth / elevation angles
    az = 2 * torch.pi * torch.rand((1, K), device=V[0].device)  # azimuth
    el = 2 * torch.pi * torch.rand((1, K), device=V[0].device)  # elevation
    # points on a unit sphere; (unit) polar to cartesian conversion
    Xin = torch.vstack([torch.cos(az) * torch.cos(el),
                        torch.sin(el),
                        torch.sin(az) * torch.cos(el)])
    return Xin


class Outputs(NamedTuple):
    R: Tensor
    t: Tensor
    X: Optional[Tensor] = None
    history: Optional[dict[str, list[Tensor]]] = None


def jrmpc(
    V: Sequence[Tensor],
    X: Optional[Tensor] = None,
    R: Optional[Tensor] = None,
    t: Optional[Tensor] = None,
    S: Optional[Tensor] = None,
    Q_factor: Optional[float] = 1000,
    max_num_iter: int = 20,
    epsilon: float = 1e-6,
    initial_priors: Optional[Tensor] = None,
    gamma: Optional[float] = None,
    update_priors: bool = False,
    progress_bar: bool = False,
) -> Outputs:
    """ JRMPC defaults arguments.

    Args:
        V (Sequence[Tensor]): Views, sequence of M point clouds of varying length (3, Nj), j=0:M.
        X (Optional[Tensor]): Cluster centers. If None, computed internally.
        R (Optional[Tensor]):
            Initial rotations (M, 3, 3). If None, initialized with the identity matrix.
        t (Optional[Tensor]):
            Initial translations (M, 3). If None, t[j] is initialized with the arithmetic mean of V[j],
            i.e. as a centering operation (typically with V[j] of shape (3, N), t[j] is V[j].mean(dim=1)).
        S (Optional[Tensor]):
            Initial variances for the K GMM components. Either a tensor (K,) or a single scalar.
            If scalar is provided then all K components are initialized with the same variance.
            If None, all variances are initialized with the same value, which is computed as the squared length of
            the diagonal of the bounding box that contains all points of V, after applying initial rototranslation.
        Q_factor (float, optional):
            After having computed Q (=1/S), it is multiplied by this factor. Default value: 1000.
        max_num_iter (Optional[int]):
            Specifies the number of iterations, Default value: 20.
        epsilon (Optional[Tensor]):
            Artificial covariance flatten. A positive number added to S, after its update, at every iteration.
            Default value: 1e-6.
        initial_priors (Optional[Tensor]):
            Specifies the prior probabilities p of the GMM components, and implicitly defines the prior p_{K+1}
            for the outlier class. It can be a (K,) tensor or a scalar. If p is scalar then that same value is
            used for all components. The sum of all elements in p (or K*p if p is scalar), must be less than 1
            as they represent a probability mass. p_{K+1} is computed internally as 1 - sum(p) if p is a vector,
            or as p_{K+1} = 1-K*p otherwise. gamma is uniquely defined from p_{K+1} as 1 = (gamma+1)*sum(p).
            Default value: The distribution of p_k is initialized as a uniform as p_k = 1/(K+1), k=0:K.
        gamma (Optional[float]):
            Positive scalar specifying the outlier proportion in V. Used to compute the prior probability
            p_{K+1} of the outlier component as gamma*sum_k(p_k). If gamma is provided then pk's are
            initialized uniformly as sum_k(p_k) = 1/(gamma+1) => p_k = 1/(K*(gamma+1)). Paramater gamma is a
            shortcut to set initialPriors uniformly, and therefore, either  'gamma' or 'initialPriors'
            should be given at a time. Default value: 1/K.
        update_priors (bool, optional):
            It is a flag that controls the update of p across iterations. The algorithm expects a scalar.
            If it is (numeric) 0 then p is kept fixed otherwise priors are updated at every iteration.
            Default value: False.
        progress_bar (bool, optional):
            If True, display a progress bar during the `max_num_iter` optimization steps.
            Default value: False.
    """
    sqe = lambda Y, X: ((Y.T[:, None, :] - X.T[None, :, :]) ** 2).sum(dim=2)
    M = len(V)
    if X is None:
        X = initialize_cluster_centers(V)
    dim, K = X.shape
    # Input checks __________________________________________________________________________________________
    assert dim == 3, 'X must be a 3 x K matrix.'
    for i, v in enumerate(V):
        assert len(v) == 3, f'V must be a sequence of M (3 x ...) matrices but V[{i}] is {tuple(v.shape)}.'
    assert len(set([v.device for v in V])) == 1, 'Views must all be on the same device.'
    if R is None:
        R = torch.eye(3, device=X.device, dtype=X.dtype).repeat(M, 1, 1)  # (M, 3, 3)
    if t is None:
        t = - torch.stack([v.mean(dim=1) for v in V]) + X.mean(dim=1)[None, :]  # (M, 3)
    if initial_priors is not None and gamma is not None:
        raise ValueError('Only one of `initial_priors` and `gamma` must be set.')
    # Init __________________________________________________________________________________________________
    TV = [R[j] @ V[j] + t[j][:, None] for j in range(M)]
    if S is not None and isinstance(S, float):
        S = torch.tensor(S).repeat(M)  # (M,)
    if S is None:
        # variance from bbox
        pointclouds = torch.hstack((*TV, X))
        min_xyz = torch.stack([coord.min() for coord in pointclouds])
        max_xyz = torch.stack([coord.max() for coord in pointclouds])
        S = sqe(min_xyz.unsqueeze(1), max_xyz.unsqueeze(1)).squeeze().repeat(K)
    S = cast(Tensor, S)
    Q = 1 / S
    Q *= Q_factor
    pk = None
    if gamma is not None:
        pk = torch.tensor(1 / (K * (gamma + 1))).repeat(K)
    if initial_priors is not None:
        # if we reach this code, gamma is None and initial_priors is not None
        if isinstance(initial_priors, float):
            initial_priors = torch.tensor(initial_priors, device=X.device).repeat(K)
        initial_priors = cast(Tensor, initial_priors)
        pk = initial_priors
        gamma = (1 - pk.sum().item()) / pk.sum().item()
    if pk is None:  # gamma and initial_priors are both None
        gamma = 1 / K
        pk = torch.tensor(1 / (K + 1), device=X.device).repeat(K)
    gamma = cast(float, gamma)  # at this point, gamma cannot be None anymore.
    # Final init
    h = 2 / Q.mean()
    beta = gamma / (h * (gamma + 1))
    # Optim _________________________________________________________________________________________________
    history = dict(R=list(), t=list())
    iterable = tqdm(range(max_num_iter)) if progress_bar else range(max_num_iter)
    for _ in iterable:
        A = [sqe(tv, X) for tv in TV]  # (M, Nj, K)
        A = [(pk * (Q ** 1.5))[None, :] * torch.exp(-0.5 * Q[None, :] * a) for a in A]  # (M, Nj, K)
        A = [a / (a.sum(dim=1)[:, None] + beta) for a in A]  # (M, Nj, K)
        # Weighted Umeyama
        Lambda = torch.stack([a.sum(dim=0) for a in A])  # (M, K)
        W = torch.stack([(v @ a) * Q for v, a in zip(V, A)])  # (M, 3, K)
        b = Lambda * Q     # (M, K)
        mW = W.sum(dim=2)  # (M, 3, K) -> (M, 3)
        mX = (X @ b.T).T   # (M, 3)
        sum_of_weights = Lambda @ Q[:, None]  # (M, K) @ (K, 1) -> (M, 1)
        # P, without considering M is:
        #       (3, K)    @ (K, 3) -         (3, 1) @ (1, 3) / (1,) -> (3, 3)
        P = X[None, :, :] @ W.mT - torch.einsum('bi, bj -> bij', mX, mW) / sum_of_weights[:, None]
        # SVD
        svd_results = torch.linalg.svd(P)
        UU, VV = svd_results.U, svd_results.Vh.mT
        UU, VV = cast(Tensor, UU), cast(Tensor, VV)  # required because C++/CUDA code is called
        SS = torch.eye(3, device=UU.device, dtype=X.dtype).repeat(M, 1, 1)
        SS[:, 2, 2] = torch.det(VV @ UU.mT)
        R = (VV @ SS @ UU.mT).mT
        t = (mX - (R @ mW[..., None]).squeeze()) / sum_of_weights
        # UPDATE
        TV = [R[j] @ V[j] + t[j][:, None] for j in range(M)]
        denominator = Lambda.sum(dim=0)  # (M, K) -> (K,)
        X = torch.stack([tv @ a for tv, a in zip(TV, A)]).sum(dim=0) / denominator[None, :]
        wnormes = torch.stack([(a * sqe(tv, X)).sum(dim=0) for a, tv in zip(A, TV)])  # (M, K)
        Q = 3 * denominator / (wnormes.sum(dim=0) + 3 * denominator * epsilon)  # (K,)
        if update_priors:
            pk = denominator / ((gamma + 1) * denominator.sum())
        history['R'].append(R.cpu())
        history['t'].append(t.cpu())
    t = t.unsqueeze(-1)
    return Outputs(R, t, X, history)
