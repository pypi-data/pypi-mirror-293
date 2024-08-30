from scipy._typing import Untyped
from .base import DenseOutput, OdeSolver

S6: Untyped
C: Untyped
E: Untyped
MU_REAL: Untyped
MU_COMPLEX: Untyped
T: Untyped
TI: Untyped
TI_REAL: Untyped
TI_COMPLEX: Untyped
P: Untyped
NEWTON_MAXITER: int
MIN_FACTOR: float
MAX_FACTOR: int

def solve_collocation_system(fun, t, y, h, Z0, scale, tol, LU_real, LU_complex, solve_lu) -> Untyped: ...
def predict_factor(h_abs, h_abs_old, error_norm, error_norm_old) -> Untyped: ...

class Radau(OdeSolver):
    y_old: Untyped
    max_step: Untyped
    f: Untyped
    h_abs: Untyped
    h_abs_old: Untyped
    error_norm_old: Untyped
    newton_tol: Untyped
    sol: Untyped
    jac_factor: Untyped
    lu: Untyped
    solve_lu: Untyped
    I: Untyped
    current_jac: bool
    LU_real: Untyped
    LU_complex: Untyped
    Z: Untyped
    def __init__(
        self,
        fun,
        t0,
        y0,
        t_bound,
        max_step=...,
        rtol: float = 0.001,
        atol: float = 1e-06,
        jac: Untyped | None = None,
        jac_sparsity: Untyped | None = None,
        vectorized: bool = False,
        first_step: Untyped | None = None,
        **extraneous,
    ): ...

class RadauDenseOutput(DenseOutput):
    h: Untyped
    Q: Untyped
    order: Untyped
    y_old: Untyped
    def __init__(self, t_old, t, y_old, Q) -> None: ...
