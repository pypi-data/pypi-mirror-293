from typing import Union, Tuple

import torch

from torchflows.bijections.continuous.base import ApproximateContinuousBijection, create_nn, RegularizedApproximateODEFunction


# https://github.com/cfinlay/ffjord-rnode/blob/master/train.py

class RNODE(ApproximateContinuousBijection):
    """Regularized neural ordinary differential equation (RNODE) architecture.

    Reference: Finlay et al. "How to train your neural ODE: the world of Jacobian and kinetic regularization" (2020); https://arxiv.org/abs/2002.02798.
    """
    def __init__(self, event_shape: Union[torch.Size, Tuple[int, ...]], **kwargs):
        n_dim = int(torch.prod(torch.as_tensor(event_shape)))
        diff_eq = RegularizedApproximateODEFunction(create_nn(n_dim, hidden_size=100, n_hidden_layers=1), regularization="sq_jac_norm")
        super().__init__(event_shape, diff_eq, **kwargs)
