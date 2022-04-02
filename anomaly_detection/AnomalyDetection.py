from AnomalyTimeSeries import AnomalyTimeSeries

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import numpy.typing as npt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")


class AnomalyDetection:
    def __init__(self, timeseries: npt.ArrayLike) -> None:
        self.timeseries = timeseries
        self.n :int = len(timeseries)
        self.beta :float = np.log(self.n) + 60
        self.F = np.full(self.n, -self.beta)
        self.change_points_array = [np.array([], dtype=int) for _ in range(self.n)]
        self.change_points_flg = np.full(self.n, 0)

    def getChangePoints(self):
        return self.change_points_array[self.n-1]


    def getChangePointsFlg(self):
        for i in self.getChangePoints():
            self.change_points_flg[i] = 1

        return self.change_points_flg


    def C(self, start, end):
        mu = 0
        cost = np.log(2*np.pi) + 1
        cost += np.log(np.sum((self.timeseries[start:end+1] - mu)**2))
        return (end - start + 1) * cost


    def fit(self):
        pass

