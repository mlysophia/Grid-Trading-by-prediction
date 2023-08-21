# _*_ coding: utf-8 _*_
"""
Time:     2023/6/20 20:46
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     get_data.py
Describe: 
"""

from jqdatasdk import *

# 登录聚宽
auth('账号', '密码')

# 获得华泰柏瑞沪深300ETF的2022年06月22日 10:00:00-2023年06月22日 10:00:00的分钟数据
data = get_price('510300.XSHG', start_date='2022-06-22 10:00:00', end_date='2023-06-22 10:00:00',
                 frequency='1m', fields=['open', 'close', 'volume', 'money'])
data.to_csv('data.csv')
