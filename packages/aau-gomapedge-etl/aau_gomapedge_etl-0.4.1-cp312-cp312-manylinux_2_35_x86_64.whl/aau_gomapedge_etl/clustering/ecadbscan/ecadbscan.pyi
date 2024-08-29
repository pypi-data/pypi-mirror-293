from numpy import float64, int32
from numpy.typing import NDArray

class EpsConstrainedAngularDBSCAN:
    def __init__(
        self, eps: float = 10, min_samples: int = 5, max_angle_diff: float = 45
    ): ...
    def run_dbscan(self, data: NDArray[float64]) -> NDArray[int32]: ...
