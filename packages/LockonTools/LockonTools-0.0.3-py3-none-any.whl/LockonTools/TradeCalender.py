#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonTools
@File    ：TradeCalender.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/1 上午9:40
@explain : 文件说明
"""
from pandas import Timestamp, to_datetime
import datetime
from numpy import datetime64
from .param import calender_days

def get_trading_calender(start_date, ndays, include_sday=True):
    """
    获取start_date之后ndays长度的交易日列表
    :param start_date:
    :type start_date:
    :param ndays:
    :type ndays:
    :return:
    :rtype:
    """
    s_date = date2datetime(start_date)
    i = ndays
    tmp = s_date
    res = []
    if include_sday:
        res.append(s_date)
    while i > 0:
        tmp = get_next_trade_date(tmp)
        res.append(tmp)
        i -= 1
    return res

def get_natural_days_diff(start_date, end_date):
    """计算 任意两天之间的自然天数
    @param start_date: 起始日 datetime.date / str
    @param end_date: 结束日 datetime.date / str
    @return: Int类型的自然天数。 For example: 60
    """
    s_date, e_date = date2datetime(start_date), date2datetime(end_date)

    return (e_date - s_date).days


def get_trading_days_diff(start_date, end_date):
    """计算出任意两天之间的交易日天数
    @param start_date: 起始日 datetime.date
    @param end_date: 结束日 datetime.date
    @return: Int类型的交易日天数。 For example: 60
    """
    s_date, e_date = date2datetime(start_date), date2datetime(end_date)
    while str(e_date) not in calender_days.keys():
        e_date = e_date + datetime.timedelta(days=1)
    while str(s_date) not in calender_days.keys():
        s_date = s_date + datetime.timedelta(days=1)
    return max(
        1, int(calender_days[str(e_date)] - calender_days[str(s_date)])
    )


def get_last_trade_date(date):
    """
    获取上一个交易日，如果date本身不为交易日，则返回上一个交易日
    :param date: T日日期
    :return: 上一个交易日
    :rtype: datetime.date
    """
    trigger = False
    date_formatted = to_datetime(date)
    while date_formatted not in calender_days.index:
        date_formatted = date_formatted - datetime.timedelta(days=1)
        trigger = True
    if trigger:
        return date2datetime(date_formatted)
    t = calender_days.index[calender_days[to_datetime(date_formatted)] - 1]

    return date2datetime(t)


def get_next_trade_date(date):
    """
    获取下一个交易日，如果date本身不为交易日，则返回下一个交易日
    :param date: T日日期
    :return: 下一个交易日
    :rtype:datetime.date
    """
    trigger = False
    date_formatted = to_datetime(date)
    while date_formatted not in calender_days.index:
        date_formatted = date_formatted + datetime.timedelta(days=1)
        trigger = True
    if trigger:
        return date2datetime(date_formatted)
    t = calender_days.index[calender_days[to_datetime(date_formatted)] + 1]
    return date2datetime(t)


def date2datetime(date):
    """
    将传入的date形式转为datetime.date
    :param date:
    :return: date的datetime形式
    :rtype: datetime.date
    """
    str_flag = False
    other_date_format_flag = False
    date_formatted = date

    if isinstance(date, datetime.date):
        return date

    if isinstance(date, Timestamp):
        date_formatted = date.to_pydatetime().date()
        other_date_format_flag = True
        return date_formatted

    if isinstance(date, datetime64):
        date_formatted = date.astype('datetime64[D]').astype(datetime.date)
        other_date_format_flag = True
        return date_formatted



    if isinstance(date, str):
        try:
            date_formatted = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            str_flag = True
        except ValueError:
            pass
        try:
            date_formatted = datetime.datetime.strptime(date, "%Y/%m/%d").date()
            str_flag = True
        except ValueError:
            pass
        try:
            date_formatted = datetime.datetime.strptime(date, "%Y%m%d").date()
            str_flag = True
        except ValueError:
            pass
        if not str_flag:
            raise ValueError("Invalid date string format %s" % date)
        else:
            if not other_date_format_flag:
                raise ValueError("Invalid date type %s" % type(date))
            return date_formatted

    else:
        return None
