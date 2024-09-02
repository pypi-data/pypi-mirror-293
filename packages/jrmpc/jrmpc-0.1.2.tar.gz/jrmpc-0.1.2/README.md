# JRMPC Numpy/PyTorch

JRMPC (Joint Registration of Multiple Point Clouds) is an algorith to jointly estimate rigid transformation aligning a set of point clouds of varying lengths.

## Installation

`pip install jrmpc`

## Presentation

This repos is a Numpy and PyTorch portage of the JRMPC algorithm.

The two reference papers are:     
- [*Georgios D. Evangelidis, D. Kounades-Bastian, R. Horaud, and E.Z Psarakis,
A Generative Model for the Joint Registration of Multiple Point Sets, ECCV, 2014.*](https://hal.science/hal-01019661v3)
- [*Georgios D. Evangelidis, R. Horaud,
Joint Alignment of Point Sets with Batch and Incremental Expectation-Maximization, PAMI, 2018.*](https://inria.hal.science/hal-01413414/file/EvangelidisHoraud-final.pdf)

The original code provided by the authors is downloadable through [this link](https://team.inria.fr/perception/files/2015/05/JRMPC_v0.9.4.zip).


## Motivation

Python is widely used in the machine learning community, far more than MATLAB.  
Leveraging PyTorch allows this implementation to support CUDA GPU. From my quick testing, **it is approximately 50x faster than the base Matlab implementation**.


## Getting started

In the simplest setup, the following code is enough:
```python
from jrmpc import jrmpc
V: list[Tensor] = load_views(...)  # list of M tensors (3, Nj).
result = jrmpc(V)
R_hat, t_hat = result.R, result.t
V_registered = [r @ v + t for v, r, t in zip(views, R_hat, t_hat)]
```

I provide a small [demo notebook](demo.ipynb) with some visualizations. 


## Multi-backend support

If you run `import jrmpc from jrmpc`, it will attempt to automatically choose a backend: `torch` if available, else `numpy`.      
If you want to manually choose a backend, run one of the following:
```python
from jrmpc.torch import jrmpc
from jrmpc.numpy import jrmpc
```


## Documentation

Here is the complete API description:


### Parameters

- **V** (`Sequence[Tensor]`): Views, sequence of $M$ point clouds of varying length `(3, Nj), j=0:M`.
- **X** (`Optional[Tensor]`): Cluster centers. If `None`, computed internally.
- **R** (`Optional[Tensor]`):
    Initial rotations `(M, 3, 3)`. If `None`, initialized with the identity matrix.
- **t** (`Optional[Tensor]`):
    Initial translations `(M, 3)`. If None, `t[j]` is initialized with the arithmetic mean of `V[j]`,
    i.e. as a centering operation.
- **S** (`Optional[Tensor]`):
    Initial variances for the `K` GMM components. Either a tensor `(K,)` or a single scalar.
    If scalar is provided then all `K` components are initialized with the same variance.
    If `None`, all variances are initialized with the same value, which is computed as the squared length of
    the diagonal of the bounding box that contains all points of `V`, after applying initial rototranslation.
- **Q_factor** (`float, optional`):
    After having computed `Q` (=`1/S`), it is multiplied by this factor. Default value: `1000`.
- **max_num_iter** (`Optional[int]`):
    Specifies the number of iterations, Default value: `100`.
- **epsilon** (`Optional[Tensor]`):
    Artificial covariance flatten. A positive number added to `S`, after its update, at every iteration.
    Default value: `1e-6`.
- **initial_priors** (`Optional[Tensor]`):
    Specifies the prior probabilities `p` of the GMM components, and implicitly defines the prior `p_{K+1}`
    for the outlier class. It can be a `(K,)` tensor or a scalar. If `p` is scalar then that same value is
    used for all components. The sum of all elements in `p` (or `K*p` if p is scalar) must be less than `1`
    as they represent a probability mass. `p_{K+1}` is computed internally as `1 - sum(p)` if p is a vector,
    or as `p_{K+1}` = `1-K\&ast;p` otherwise. gamma is uniquely defined from `p_{K+1}` as `1 = (gamma+1)&ast;sum(p)`.
    Default value: The distribution of `p_k` is initialized as a uniform as `p_k = 1/(K+1), k=0:K`.
- **gamma** (`Optional[float]`):
    Positive scalar specifying the outlier proportion in `V`. Used to compute the prior probability
    `p_{K+1}` of the outlier component as `gamma*sum_k(p_k)`. If gamma is provided then `pk's` are
    initialized uniformly as `sum_k(p_k) = 1/(gamma+1)` => `p_k = 1/(K*(gamma+1))`. Paramater gamma is a
    shortcut to set `initial_priors` uniformly, and therefore, either  `gamma` or `initialPriors`
    should be given at a time. Default value: `1/K`.
- **update_priors** (`bool, optional`):
    If True, priors are updated at every iteration.
    Default value: `False`.
- **progress_bar** (`bool, optional`):
    If `True`, display a progress bar during the `max_num_iter` optimization steps.
    Default value: `False`.

### Returns

A named tuple with four elements:
1. R: estimated rotation matrices to align the given views onto the estimated template. Tensor `(M, 3, 3)`.
2. t: estimated translation vector to align the given views onto the estimated template. Tensor `(M, 3, 1)`.
3. X: estimated template. Point clouds `(M, K)`.
4. history: the transformation parameters after each iteration. Dictionary with keys `R` and `t`. 
`history['R']` and `history['t']` are list of length `max_num_iter` of rotation and translation tensors. 