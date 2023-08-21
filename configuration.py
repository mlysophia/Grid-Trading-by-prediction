# _*_ coding: utf-8 _*_
"""
Time:     2023/6/20 11:46
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     configuration.py
Describe: 
"""


# 预测波动标准差和涨跌的参数 ################################################################################################
span_pred = 10  # use 10 minutes for predicting volatility and trend

span_pred_vol = 10  # use 10 minutes as window for predicting volatility
pred_vol_method = 'ewma'  # param can be 'ewma', 'Garch', 'cons'
default_vol = 0.001  # default volatility for method 'cons'

span_pred_trend = 5  # use 5 minutes as window for predicting trend
pred_trend_method = 'rsi'  # param can be 'moving_average', 'rsi', 'no_trend_factor'

# 网格参数 ##############################################################################################################
num_orders = 10  # 单侧的网格数量
grid_method = 'uni'  # param can be 'uni', 'geo'
conservative_factor = 3  # when trend is positive, grid_width will be adjusted to conservative_factor * grid_width
# for grids above the baseline, and when trend is negative, grid_width below the baseline will be adjusted
vol_factor = 1  # 给预测的波动标准差乘的系数

# 测试参数 ##############################################################################################################
total_fund = 10000000  # 总资金
init_position = 1/2  # 初始仓位

