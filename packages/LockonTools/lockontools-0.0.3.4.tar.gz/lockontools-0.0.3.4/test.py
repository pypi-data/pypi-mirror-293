#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：LockonTools 
@File    ：test.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/1 上午10:05 
@explain : 文件说明
'''
import src.LockonTools as lt
import datetime
import pandas as pd
#%%
date1 = '20240101'
date2 = datetime.date(2024,7,2)
lt.get_last_trade_date(date1)
lt.get_next_trade_date(date1)
lt.get_trading_days_diff(date1,date2)
# %%
import src.LockonTools.EmlReader as er

reader1 = er.MailReader('./【银河证券】场外交易估值明细日报.eml')
reader2 = er.MailReader('./20240628-互换合约-风控.eml')