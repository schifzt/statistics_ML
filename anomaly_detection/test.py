from AnomalyTimeSeries import AnomalyTimeSeries
from OptimalPartition import OptimalPartition
from PELT import PELT

import numpy as np
np.set_printoptions(precision=3, suppress=True)
import numpy.typing as npt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
import time


if __name__ == '__main__':

    n = 1000

    ts = AnomalyTimeSeries(n)
    x = ts.getTimeSeries()

    ads = [OptimalPartition(x), PELT(x)]

    for i, ad in enumerate(ads):
        start = time.time()
        ad.fit()
        end = time.time()

        print(ts.getChangePoints())
        print(ad.getChangePoints())
        print(ts.getDeviations())
        print(f"elapsed time: {end - start}")


    linestyle = ['dashed', 'dotted']
    sns.lineplot(data=x, linewidth=1, alpha = 0.5)
    for cp in ts.getChangePoints():
        plt.axvline(x=cp, ymin=0, ymax=2, linewidth=1, linestyle='solid', color='green')
    for i, ad in enumerate(ads):
        for cp in ad.getChangePoints():
            plt.axvline(x=cp, ymin=0, ymax=2, linewidth=1, linestyle=linestyle[i])
    plt.show()