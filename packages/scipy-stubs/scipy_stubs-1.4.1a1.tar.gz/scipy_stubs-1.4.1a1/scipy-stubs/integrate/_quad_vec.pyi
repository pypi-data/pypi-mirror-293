import collections
from typing_extensions import override

from scipy._typing import Untyped

class LRUDict(collections.OrderedDict[tuple[float, float], Untyped]):
    def __init__(self, max_size: int) -> None: ...
    @override
    def update(self, other) -> None: ...  # type: ignore[override]

class SemiInfiniteFunc:
    def __init__(self, func, start, infty) -> None: ...
    def get_t(self, x) -> Untyped: ...
    def __call__(self, t) -> Untyped: ...

class DoubleInfiniteFunc:
    def __init__(self, func) -> None: ...
    def get_t(self, x) -> Untyped: ...
    def __call__(self, t) -> Untyped: ...

class _Bunch:
    def __init__(self, **kwargs) -> None: ...

def quad_vec(
    f,
    a,
    b,
    epsabs: float = 1e-200,
    epsrel: float = 1e-08,
    norm: str = "2",
    cache_size: float = ...,
    limit: int = 10000,
    workers: int = 1,
    points: Untyped | None = None,
    quadrature: Untyped | None = None,
    full_output: bool = False,
    *,
    args=(),
) -> Untyped: ...
