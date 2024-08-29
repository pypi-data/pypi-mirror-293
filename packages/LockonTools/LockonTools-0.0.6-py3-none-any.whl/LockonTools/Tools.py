#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonTools
@File    ：Tools.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/18 下午2:33
@explain : 文件说明
"""
# %%
import shutil

# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import warnings
import time
import os
import datetime


class WarningFilter:
    """
    用于忽略Warning
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
        print("time cost:  %.6f seconds" % total_time)
        return result

    return decorator


class TimeCounter:
    """
    用于计时，用法:
    with Timecounter():
        run()
    """

    def __enter__(self):
        self.s_time = time.perf_counter()

    def __exit__(self, type, value, traceback):
        print("time cost: %.3f" % (time.perf_counter() - self.s_time))


def get_fp_creation_time(fp):
    """
    获取指定位置文件创建的时间
    :param fp: 文件路径
    :type fp: str
    :return: 文件创建的时间
    :rtype:  datetime.datetime
    """
    if not os.path.exists(fp):
        raise ValueError("文件夹路径不存在,先导出文件夹到桌面")
    # 获取文件的创建时间戳
    creation_time = os.path.getctime(fp)

    # 将时间戳转换为本地时间
    dt_object = datetime.datetime.fromtimestamp(creation_time)

    return dt_object


def copy_dir2path(src_dir_fp, dst_dir_fp, cpy_type="replace"):
    """
    复制文件夹到指定位置
    :param src_dir_fp: 源文件夹路径
    :type src_dir_fp: str
    :param dst_dir_fp: 目标文件夹路径
    :type dst_dir_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_dir_fp):
        shutil.rmtree(dst_dir_fp)
    shutil.copytree(src_dir_fp, dst_dir_fp)
    return f"Successfully copied {src_dir_fp} to {dst_dir_fp}"


def move_dir2path(src_dir_fp, dst_dir_fp, cpy_type="replace"):
    """
    移动文件夹到指定位置
    :param src_dir_fp: 源文件夹路径
    :type src_dir_fp: str
    :param dst_dir_fp: 目标文件夹路径
    :type dst_dir_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_dir_fp):
        shutil.rmtree(dst_dir_fp)
    shutil.move(src_dir_fp, dst_dir_fp)
    return f"Successfully moved {src_dir_fp} to {dst_dir_fp}"


def move_file2path(src_fp, dst_fp, cpy_type="replace"):
    """
    移动文件到指定位置
    :param src_fp: 源文件路径
    :type src_fp: str
    :param dst_fp: 目标文件路径
    :type dst_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_fp):
        os.remove(dst_fp)
    shutil.move(src_fp, dst_fp)
    return f"Successfully moved {src_fp} to {dst_fp}"


def copy_file2path(src_fp, dst_fp, cpy_type="replace"):
    """
    复制文件到指定位置
    :param src_fp: 源文件路径
    :type src_fp: str
    :param dst_fp: 目标文件路径
    :type dst_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_fp):
        os.remove(dst_fp)
    shutil.copy2(src_fp, dst_fp)
    return f"Successfully copied {src_fp} to {dst_fp}"
