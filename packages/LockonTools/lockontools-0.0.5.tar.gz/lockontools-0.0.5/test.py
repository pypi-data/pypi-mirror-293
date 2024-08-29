#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：LockonTools 
@File    ：test.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/11 上午11:34 
@explain : 文件说明
'''
# %%
import src.LockonTools as LT
date1 = '2024-06-01'
date2 = '2024-07-02'
d1 = LT.date2dtdate(date1)
LT.get_trading_calender(d1,20)
