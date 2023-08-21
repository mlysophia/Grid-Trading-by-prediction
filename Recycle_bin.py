# _*_ coding: utf-8 _*_
"""
Time:     2023/6/22 22:36
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     Recycle_bin.py
Describe: 
"""

# volume ###############################################################################################################
def volume(data):
    money = pd.Series(data[-1])  # 提取‘money’列
    vol = pd.Series(data[-2])  # 提取‘volume’列
    prices = money / vol
    price_diff = prices.shift(-1) - prices  # 计算价格的一阶差分
    volume_diff = vol.shift(-1) - vol  # 计算成交量的一阶差分

    # 计算价格和成交量变动的乘积
    change_product = price_diff * volume_diff

    # 判断涨跌趋势
    trend = 0
    for val in change_product:
        if val > 0:
            trend += 1  # 上涨
        elif val < 0:
            trend += -1  # 下跌
        else:
            trend += 0

    if trend > 0:
        return 1
    elif trend < 0:
        return -1
    else:
        return 0
