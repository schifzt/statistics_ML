from AnomalyTimeSeries import AnomalyTimeSeries
from AnomalyDetection import AnomalyDetection

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import numpy.typing as npt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
import itertools
import time


"""
Implementaiton of this paper:
    Optimal detection of changepoints with a linear computational cost
    https://www.jstor.org/stable/23427357
"""


class PELT(AnomalyDetection):
    def __init__(self, timeseries: npt.ArrayLike):
        super().__init__(timeseries)


    def fit(self):
        pts = [0]
        for tau_ast in range(1,self.n):
            pts.extend([0, tau_ast-1])
            self.F[tau_ast] = np.min(
                [self.F[tau] + self.C(tau+1, tau_ast) + self.beta \
                    for tau in pts]
            )
            tau_prime = np.argmin(
                [self.F[tau] + self.C(tau+1, tau_ast) + self.beta \
                    for tau in range(tau_ast)]
            )

            self.change_points_array[tau_ast] = \
                np.append(self.change_points_array[tau_prime], tau_prime)

            pts = [tau for tau in range (tau_ast) \
                if self.F[tau] + self.C(tau+1, tau_ast) > self.F[tau_ast]]

            # print(f"tau_ast: {tau_ast}")
            # print(f"obj: {obj}")
            # print(f"tau_prime: {tau_prime}")
            # print(f"self.F: {self.F}")
            # print(self.change_points_array[tau_ast])
            # print(f"pts: {pts}")
            # print("---\n")


if __name__ == '__main__':

    n = 1000

    ts = AnomalyTimeSeries(n)
    x = ts.getTimeSeries()

    ad = PELT(x)
    start = time.time()
    ad.fit()
    end = time.time()

    df = pd.DataFrame(data={
        'x': x,
        'change_points_flg': ts.getChangePointsFlg(),
        'estimated_change_points_flg': ad.getChangePointsFlg(),
        })

    print(ts.getChangePoints())
    print(ad.getChangePoints())
    print(ts.getDeviations())

    print(f"elapsed time: {end - start}")

    sns.lineplot(data=df['x'], linewidth=1, alpha = 0.5)

    for i, (cp1, cp2) in enumerate(itertools.pairwise(ts.getChangePoints())):
        if i % 2:
            plt.axvspan(xmin=cp1, xmax=cp2, alpha = 0.1)
        else:
            plt.axvspan(xmin=cp1, xmax=cp2, alpha = 0.1, color = "pink")

    cp = ad.getChangePoints()[0]
    plt.axvline(x=cp, ymin=0.0, ymax=0.2, linewidth=1.5, linestyle='solid', label = 'estimated')
    for cp in ad.getChangePoints()[1:]:
        plt.axvline(x=cp, ymin=0.0, ymax=0.2, linewidth=1.5, linestyle='solid')

    plt.legend()
    plt.show()


