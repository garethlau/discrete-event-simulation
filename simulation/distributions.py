import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Distribution():
    def __init__(self, distribution):
        self.distribution = distribution
        self.intervals = np.diff(distribution)

    def next(self, curr):
        for i in self.distribution:
            if (curr < i):
                return i

    def get_interval(self):
        return np.delete(self.intervals, 0)[0]

if __name__ == '__main__':
    np.random.seed(42)
    n = np.random.normal(size=50, loc=19 * 60, scale=200)
    u = np.random.uniform(size=50, low=11 * 60, high=24 * 60)

    c = np.concatenate((u, n), axis=0)
    c = np.sort(c)
    print(c)
    sns.set(color_codes=True)
    sns.distplot(c, bins=24)
    plt.show()
    d = Distribution(c)

    curr = 0
    while (curr < 24 * 60):
        next_arrival = d.next(curr)
        t = next_arrival - curr
        curr = next_arrival
        print("Time to next arrival: {}".format(t))