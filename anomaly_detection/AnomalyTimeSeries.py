import numpy as np
np.set_printoptions(precision=3, suppress=True)
import numpy.typing as npt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")


class AnomalyTimeSeries:
    def __init__(self, n) -> None:
        self.n = n

        generator = self.__generator_closure()
        self.time_series = np.array([generator() for t in range(self.n)])


    # def getGenerator(self):
    #     generateDatam = self.__generator_closure()
    #     return generateDatam


    def getTimeSeries(self):
        return self.time_series


    def getChangePoints(self):
        return self.change_points


    def getChangePointsFlg(self):
        return self.change_points_flg


    def getDeviations(self):
        return self.deviations


    def __setChangePoints(self):
        # -------------------------------------------
        # 変化点を設定する
        #   [2, n-2]の一様分布からn/50個の変化点を生成
        #   間隔は30以上
        #
        # 生成方法（その1）
        #   まず狭いレンジでnum個変化点を生成して、次に間隔がdistance以上になるように間隔を押し広げる
        #   https://stackoverflow.com/questions/51918580/python-random-list-of-numbers-in-a-range-keeping-with-a-minimum-distance
        #
        # 生成方法（その2）
        #   30以上hoge以下の乱数を変化点の間隔としてnum個生成して、その累積和をとる
        # -------------------------------------------
        self.change_points = []
        self.change_points_flg = np.zeros(self.n, dtype=int)

        distance = 30
        num = int(self.n/50)
        lb = 2
        ub = num + distance - 1
        # self.change_points = np.array([(distance-1)*i + x for i, x in enumerate(sorted(np.random.randint(lb, ub, num)))])
        self.change_points = [i for i in np.cumsum(np.random.randint(30, 100, num)) if i < self.n]

        self.change_points = np.insert(self.change_points, 0, 0, axis=0)
        self.change_points = np.append(self.change_points, self.n-1)

        for point in self.change_points:
            self.change_points_flg[point] = 1


    def __generator_closure(self):
        t = -1
        mu, sd = 0, 1

        self.deviations = []
        self.__setChangePoints()

        def generateDatam():
            nonlocal t, sd
            t = t+1

            if self.change_points_flg[t] == 1:
                sd = np.random.lognormal(0, np.log(10)/2)
                self.deviations.append(sd)

            return np.random.normal(mu, sd)

        return generateDatam



if __name__ == '__main__':
    n = 1000
    ts = AnomalyTimeSeries(n)

    df = pd.DataFrame(data={
        'x': ts.getTimeSeries(),
        'change_points_flg': ts.getChangePointsFlg()
        })

    print(ts.getChangePoints())
    print(ts.getDeviations())

    sns.lineplot(data=df['x'], linewidth=1, alpha = 0.5)
    plt.show()