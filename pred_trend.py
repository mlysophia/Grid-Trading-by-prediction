# _*_ coding: utf-8 _*_
"""
Time:     2023/6/21 13:31
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     pred_trend.py
Describe: 
"""

import numpy as np
import pandas as pd
from configuration import span_pred_trend


# moving_average #######################################################################################################
def moving_average(prices):
    if prices.iloc[-1] > prices.mean():
        return 1
    elif prices.iloc[-1] < prices.mean():
        return -1
    else:
        return 0


# rsi ##################################################################################################################
def rsi(prices):
    price_diff = prices.diff(1)  # 计算价格的一阶差分
    up_gain = price_diff.where(price_diff > 0, 0)  # 上涨幅度
    down_loss = -price_diff.where(price_diff < 0, 0)  # 下跌幅度
    avg_gain = up_gain.rolling(window=span_pred_trend).mean()  # 平均上涨幅度
    avg_loss = down_loss.rolling(window=span_pred_trend).mean()  # 平均下跌幅度
    rs = avg_gain / avg_loss  # 相对强度
    rsi_flag = 100 - (100 / (1 + rs))  #

    if rsi_flag.iloc[-1] < 30:
        return 1
    elif rsi_flag.iloc[-1] > 70:
        return -1
    else:
        return 0
