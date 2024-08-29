from typing import Callable, Sequence

import numpy as np
from duckdb import DuckDBPyConnection, DuckDBPyRelation

from aau_gomapedge_etl.clustering import (
    EpsConstrainedAngularDBSCAN,
    WeightedDirectionalDBSCAN,
)

from .protocol import Grouper

Strategy = Callable[[list[tuple[float, float, float]]], list[int]]


class WDDBSCANStrategy:
    def __init__(
        self, max_distance: float, min_samples: int, directional_weight: float
    ):
        self.__cluster = WeightedDirectionalDBSCAN(
            max_distance, min_samples, directional_weight
        )

    def __call__(self, data: list[tuple[float, float, float]]) -> list[int]:
        return self.__cluster.fit_predict(data).tolist()


class ECADBSCANStrategy:
    def __init__(self, max_distance: float, max_angle: float, min_samples: int):
        self.__cluster = EpsConstrainedAngularDBSCAN(
            max_distance, min_samples, max_angle
        )

    def __call__(self, data: list[tuple[float, float, float]]) -> list[int]:
        return self.__cluster.run_dbscan(np.array(data)).tolist()


class DefaultDuckDbGrouper(Grouper):
    __slots__ = ["__con", "__max_dist", "__max_angle", "__min_samples"]

    def __init__(self, con: DuckDBPyConnection, strategy: Strategy) -> None:
        self.__con = con
        self._strategy = strategy

    def group(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        data = self.__con.execute(
            f"""
SELECT list(id ORDER BY id)                                        AS ids,
       list([ST_X(location), ST_Y(location), heading] ORDER BY id) AS data
FROM tbl
GROUP BY cls
"""
        )
        ids = np.empty(0, dtype=int)
        cids = np.empty(0, dtype=int)

        for row in data.fetchall():
            dims = row[1]
            ids = np.append(ids, row[0])
            cids = np.append(
                cids,
                self._strategy(dims),
            )

        result = np.array((ids, cids))
        self.__con.execute(
            f"""
CREATE OR REPLACE TABLE detection AS

    SELECT column0 AS id, 
        column1 AS cid,
        trip_no,
        img_seq_id,
        heading,
        width,
        height,
        score,
        cls,
        location
    FROM result
        INNER JOIN tbl ON column0 = id;
"""
        )

        return self.__con.table("detection").filter("cid > -1")
