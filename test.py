# _*_ coding: utf-8 _*_
"""
Time:     2023/6/24 18:01
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     test.py
Describe: 
"""

import pandas as pd
import matplotlib.pyplot as plt
from GridTrade_ETF import backtest

#  get data
# 获得华泰柏瑞沪深300ETF的2022年06月22日 10:00:00-2023年06月22日 10:00:00的分钟数据
df = pd.read_csv('GridTrade_ETFmin/data.csv')

test_result = backtest(df)
