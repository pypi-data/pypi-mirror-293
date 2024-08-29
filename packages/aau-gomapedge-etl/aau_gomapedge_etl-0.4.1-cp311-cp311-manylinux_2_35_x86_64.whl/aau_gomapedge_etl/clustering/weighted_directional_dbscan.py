from typing import Sequence, TypeVar

import numpy as np
from numpy import ndarray
from numpy.typing import NDArray
from sklearn.cluster import DBSCAN

T = TypeVar("T", float, NDArray)


# Not threadsafe
class WeightedDirectionalDBSCAN:
    def __init__(
        self,
        max_distance: float = 10,
        min_samples: int = 5,
        direction_weight: float = 1,
    ) -> None:
        if max_distance <= 0:
            raise ValueError("max_distance must be a float >0.0")
        self.max_distance = max_distance
        self.min_samples = min_samples
        self.direction_weight = direction_weight

        self.__dbscan = DBSCAN(
            eps=self.max_distance,
            min_samples=self.min_samples,
        )

    def fit_predict(
        self, X: Sequence[tuple[float, float, float]] | NDArray, y=None
    ) -> ndarray:
        if not isinstance(X, ndarray):
            X = np.array(X)

        radians = np.radians(X[:, 2])
        x = np.cos(radians) * self.direction_weight
        y = np.sin(radians) * self.direction_weight
        X = np.column_stack((X[:, :2], x, y))

        self.__dbscan.fit(X)
        return self.__dbscan.labels_
