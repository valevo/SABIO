import numpy as np


class Model:
    def __init__(self):
        pass
    
    @staticmethod
    def identity(x): return x

    # a1
    @staticmethod
    def absolute_value(x): return abs(x)
    
    # a2
    # q=99.5 (empirically) leads to 1% of the data being outside the range
    @staticmethod
    def percentile_norm(v, q=99.5):
        return (v - np.percentile(v, 100-q))/(np.percentile(v, q) - np.percentile(v, 100-q))

    # a3
    # = a2(a1(x))
    def normed_abs(self, x, q=100): return self.percentile_norm(self.absolute_value(x), q=q)
    
    # 1 - a3 = 1 - a2(a1(x))
    def inv_normed_abs(self, x, q=100):
        return 1 - self.normed_abs(x, q=q)