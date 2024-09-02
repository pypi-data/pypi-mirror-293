from __future__ import annotations
from tqdm.auto import tqdm
from typing import Sequence, Optional, NamedTuple, cast
import numpy as np
from numpy.typing import NDArray


def initialize_cluster_centers(V: Sequence[NDArray]) -> NDArray:
    # In all generality, inputs can be a sequence of point clouds of varying lengths.
    # We set K as the 50% of the median cardinality of the views
    K = int(0.5 * np.median(np.array([p.shape[1] for p in V])))
    # To initialize cluster centers, we sample the unit sphere,
    # by randomly selecting azimuth / elevation angles
    az = 2 * np.pi * np.random.rand(1, K)  # azimuth
    el = 2 * np.pi * np.random.rand(1, K)  # elevation
    # points on a unit sphere; (unit) polar to cartesian conversion
    Xin = np.vstack((np.cos(az) * np.cos(el),
                     np.sin(el),
                     np.sin(az) * np.cos(el)))
    return Xin


class Outputs(NamedTuple):
    R: NDArray
    t: NDArray
    X: Optional[NDArray] = None
    history: Optional[dict[str, list[NDArray]]] = None


def jrmpc(
    V: Sequence[NDArray],
    X: Optional[NDArray] = None,
    R: Optional[NDArray] = None,
    t: Optional[NDArray] = None,
    S: Optional[NDArray] = None,
    Q_factor: float = 1000,
    max_num_iter: int = 20,
    epsilon: float = 1e-6,
    initial_priors: Optional[NDArray] = None,
    gamma: Optional[float] = None,
    update_priors: bool = False,
    progress_bar: bool = False,
) -> Outputs:
    """ JRMPC defaults arguments.

    Args:
        V (Sequence[NDArray]): Views, sequence of M point clouds of varying length (3, Nj), j=0:M.
        X (Optional[NDArray]): Cluster centers. If None, computed internally.
        R (Optional[NDArray]):
            Initial rotations (M, 3, 3). If None, initialized with the identity matrix.
        t (Optional[NDArray]):
            Initial translations (M, 3). If None, t[j] is initialized with the arithmetic mean of V[j],
            i.e. as a centering operation (typically with V[j] of shape (3, N), t[j] is V[j].mean(axis=1)).
        S (Optional[NDArray]):
            Initial variances for the K GMM components. Either a tensor (K,) or a single scalar.
            If scalar is provided then all K components are initialized with the same variance.
            If None, all variances are initialized with the same value, which is computed as the squared length of
            the diagonal of the bounding box that contains all points of V, after applying initial rototranslation.
        Q_factor (float, optional):
            After having computed Q (=1/S), it is multiplied by this factor. Default value: 1000.
        max_num_iter (Optional[int]):
            Specifies the number of iterations, Default value: 20.
        epsilon (Optional[NDArray]):
            Artificial covariance flatten. A positive number added to S, after its update, at every iteration.
            Default value: 1e-6.
        initial_priors (Optional[NDArray]):
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
    sqe = lambda Y, X: ((Y.T[:, None, :] - X.T[None, :, :]) ** 2).sum(axis=2)
    M = len(V)
    if X is None:
        X = initialize_cluster_centers(V)
    dim, K = X.shape
    # Input checks __________________________________________________________________________________________
    assert dim == 3, 'X must be a 3 x K matrix.'
    for i, v in enumerate(V):
        assert len(v) == 3, f'V must be a sequence of M (3 x ...) matrices but V[{i}] is {tuple(v.shape)}.'
    if R is None:
        R = np.tile(np.eye(3, dtype=X.dtype), (M, 1, 1))  # (M, 3, 3)
    if t is None:
        t = - np.stack([v.mean(axis=1) for v in V]) + X.mean(axis=1)[None, :]  # (M, 3)
        t = cast(NDArray, t)
    if initial_priors is not None and gamma is not None:
        raise ValueError('Only one of `initial_priors` and `gamma` must be set.')
    # Init __________________________________________________________________________________________________
    TV = [R[j] @ V[j] + t[j][:, None] for j in range(M)]
    if S is not None and isinstance(S, float):
        S = np.tile(np.asarray(S), M)  # (M,)
    if S is None:
        # variance from bbox
        pointclouds = np.hstack((*TV, X))
        min_xyz = np.stack([coord.min() for coord in pointclouds])
        max_xyz = np.stack([coord.max() for coord in pointclouds])
        S = np.tile(sqe(min_xyz[:, None], max_xyz[:, None]).squeeze(), K)
    Q = 1 / S
    Q *= Q_factor
    pk = None
    if gamma is not None:
        pk = np.tile(np.asarray(1 / (K * (gamma + 1))), K)
    if initial_priors is not None:
        # if we reach this code, gamma is None and initial_priors is not None
        if isinstance(initial_priors, float):
            initial_priors = np.tile(np.asarray(initial_priors), K)
        pk = initial_priors
        gamma = (1 - pk.sum().item()) / pk.sum().item()
    if pk is None:  # gamma and initial_priors are both None
        gamma = 1 / K
        pk = np.tile(np.asarray(1 / (K + 1)), K)
    gamma = cast(float, gamma)  # at this point, gamma cannot be None anymore.
    # Final init
    h = 2 / Q.mean()
    beta = gamma / (h * (gamma + 1))
    # Optim _________________________________________________________________________________________________
    history = dict(R=list(), t=list())
    iterable = tqdm(range(max_num_iter)) if progress_bar else range(max_num_iter)
    for _ in iterable:
        A = [sqe(tv, X) for tv in TV]  # (M, Nj, K)
        A = [(pk * (Q ** 1.5))[None, :] * np.exp(-0.5 * Q[None, :] * a) for a in A]  # (M, Nj, K)
        A = [a / (a.sum(axis=1)[:, None] + beta) for a in A]  # (M, Nj, K)
        # Weighted Umeyama
        Lambda = np.stack([a.sum(axis=0) for a in A])  # (M, K)
        W = np.stack([(v @ a) * Q for v, a in zip(V, A)])  # (M, 3, K)
        b = Lambda * Q      # (M, K)
        mW = W.sum(axis=2)  # (M, 3, K) -> (M, 3)
        mX = (X @ b.T).T    # (M, 3)
        sum_of_weights = Lambda @ Q[:, None]  # (M, K) @ (K, 1) -> (M, 1)
        # P, without considering M is:
        #       (3, K)    @ (K, 3) -         (3, 1) @ (1, 3) / (1,) -> (3, 3)
        P = X[None, :, :] @ W.swapaxes(1, 2) - np.einsum('bi, bj -> bij', mX, mW) / sum_of_weights[:, None]
        # SVD
        UU, _, VVh = np.linalg.svd(P)
        VV = VVh.swapaxes(1, 2)
        SS = np.tile(np.eye(3, dtype=X.dtype), (M, 1, 1))
        SS[:, 2, 2] = np.linalg.det(VV @ UU.swapaxes(1, 2))
        R = (VV @ SS @ UU.swapaxes(1, 2)).swapaxes(1, 2)
        t = (mX - (R @ mW[..., None]).squeeze()) / sum_of_weights
        R, t = cast(NDArray, R), cast(NDArray, t)
        # UPDATE
        TV = [R[j] @ V[j] + t[j][:, None] for j in range(M)]
        denominator = Lambda.sum(axis=0)  # (M, K) -> (K,)
        X = np.stack([tv @ a for tv, a in zip(TV, A)]).sum(axis=0) / denominator[None, :]
        X = cast(NDArray, X)
        wnormes = np.stack([(a * sqe(tv, X)).sum(axis=0) for a, tv in zip(A, TV)])  # (M, K)
        Q = 3 * denominator / (wnormes.sum(axis=0) + 3 * denominator * epsilon)  # (K,)
        if update_priors:
            pk = denominator / ((gamma + 1) * denominator.sum())
        history['R'].append(R)
        history['t'].append(t)
    t = t[..., None]
    return Outputs(R, t, X, history)
