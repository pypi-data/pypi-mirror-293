#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：LockonTools 
@File    ：Tools.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/1 上午11:05 
@explain : 文件说明
'''
import warnings


class WarningFilter:
    def __enter__(self):
        self.old_filters = warnings.filters
        warnings.filterwarnings("ignore", category=UserWarning)

    def __exit__(self, type, value, traceback):
        warnings.filters = self.old_filters
