#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonTools
@File    ：Tools.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/1 上午11:05
@explain : 文件说明
"""
import warnings
import time


class WarningFilter:
    """
    with WarningFilter():
        df = pd.read_excel(io.BytesIO(attr_data))
    """

    def __enter__(self):
        self.old_filters = warnings.filters
        warnings.filterwarnings("ignore", category=UserWarning)

    def __exit__(self, type, value, traceback):
        warnings.filters = self.old_filters


def print_calc_time(func):
    """此函数为python修饰符，用于计算目标函数执行的时间
    usage:
        @printCalcTime
        def getPricePathByNumpy(spot, volatility, tau, steps):
            simulationTimes = publicParams.simulationTimes
            dt = tau / steps
            S = np.zeros((steps+1, simulationTimes))
            S[0] = spot
        #     np.random.seed(2000)
            for t in range(1, steps+1):
                z = np.random.standard_normal(simulationTimes)
                S[t] = S[t-1] * np.exp((publicParams.rf- 0.5 * volatility **2)* dt + volatility * np.sqrt(dt)*z)
            return S
    """

    def decorator(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        print('pricing cost:  %.6f seconds' % total_time)
        return result

    return decorator
