# coding=utf-8

import pandas as pd
import numpy as np


def get_confidence(filepath):
    ASCfile = pd.read_csv(filepath, skiprows=6, engine='python', sep=' ', delimiter=None, index_col=False, header=None, skipinitialspace=True)

    ndarray = ASCfile.as_matrix().reshape(1, -1)
    ndarray.sort()
    ndarray = ndarray[ndarray>=-1] # 取正常的NDVI值
    q_5 = np.percentile(ndarray, 5)
    q_95 = np.percentile(ndarray, 95)

    return q_5, q_95