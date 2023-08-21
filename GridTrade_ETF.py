# _*_ coding: utf-8 _*_
"""
Time:     2023/6/13 13:47
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     GridTrade_ETF.py
Describe: 
"""

import pandas as pd
import numpy as np
import arch
from pred_trend import moving_average, rsi
from generate_grid import generate_uni_grid, generate_geo_grid, generate_position
from configuration import span_pred, pred_vol_method, pred_trend_method, grid_method, default_vol, num_orders, \
    total_fund, init_position


#  predict std
def pred_vol(prices):
    if pred_vol_method == 'ewma':
        size_vol = prices.ewm(span=span_pred, adjust=False).std()
    elif pred_vol_method == 'Garch':
        size_vol = (1000 * prices).rolling(window=span_pred) \
                       .apply(lambda x: arch.arch_model(x).fit(disp='off').forecast(horizon=1)
                              .variance.iloc[-1, 0] ** 0.5) / 1000
    else:
        size_vol = default_vol

    size_vol = np.maximum(size_vol, default_vol)

    return size_vol


#  predict the trend
def pred_trend(prices):
    if pred_trend_method == 'moving_average':
        trend_flag = prices.rolling(span_pred).apply(moving_average)
    elif pred_trend_method == 'rsi':
        trend_flag = prices.rolling(span_pred).apply(rsi)
    else:
        trend_flag = 0

    return trend_flag


# generate grid
def generate_grid(price, vol, trend):
    if grid_method == 'uni':
        grids = generate_uni_grid(price, vol, trend)
    elif grid_method == 'geo':
        grids = generate_geo_grid(price, vol, trend)
    else:
        grids = generate_uni_grid(price, vol, trend)

    return grids


# back_testing
def backtest(data):
    # 预测波动性与涨跌
    vol_pred = pred_vol(data['open']).fillna(default_vol)
    trend_pred = pred_trend(data['open']).fillna(0)

    backtest_result = pd.DataFrame({'price': data['open'].copy(), 'volatility': vol_pred, 'trend': trend_pred})
    backtest_result['security_amount'] = None
    backtest_result['last_trade_price'] = None
    backtest_result['available_fund'] = None
    backtest_result['total_value'] = None

    # initialize
    # 初始仓位为init_position
    backtest_result['security_amount'].iloc[0] = np.floor(total_fund * init_position /
                                                          (backtest_result['price'].iloc[0] * 100))
    # 初始价格基准线为当前价格
    backtest_result['last_trade_price'].iloc[0] = backtest_result['price'].iloc[0].copy()
    # 初始化可用资金
    backtest_result['available_fund'].iloc[0] = total_fund - backtest_result['security_amount'].iloc[0] * 100 * \
                                                backtest_result['price'].iloc[0]
    # 初始化总资产
    backtest_result['total_value'].iloc[0] = total_fund

    # 遍历每分钟数据
    for i in range(1, len(data)):
        present_price = backtest_result['price'].iloc[i].copy()
        base_price = backtest_result['last_trade_price'].iloc[i - 1].copy()
        vol = backtest_result['volatility'].iloc[i].copy()
        trend = backtest_result['trend'].iloc[i].copy()

        # 生成新的网格
        grids = generate_grid(base_price, vol, trend)

        # 生成调仓信号
        position_flag = generate_position(present_price, grids)

        # 生成交易信号
        # 根据交易信号应执行的交易
        delta_flag = np.floor(backtest_result['total_value'].iloc[i - 1] * position_flag /
                              (2 * num_orders * backtest_result['price'].iloc[i] * 100))

        # 实际应执行的交易
        if position_flag > 0:
            # 若买入，计算资金允许的最大买入量
            max_delta = np.floor(backtest_result['available_fund'].iloc[i - 1] /
                                 (backtest_result['price'].iloc[i] * 100))
            delta = min(delta_flag, max_delta)
        else:
            # 若卖出，计算持仓允许的最大卖出量
            delta = -min(abs(delta_flag), backtest_result['security_amount'].iloc[i - 1])

        # test
        if delta != 0:
            print(grids, position_flag, delta_flag, delta, backtest_result['total_value'].iloc[i-1])

        # 执行交易
        if delta != 0:
            backtest_result['security_amount'].iloc[i] = backtest_result['security_amount'].iloc[i - 1] + delta
            backtest_result['last_trade_price'].iloc[i] = backtest_result['price'].iloc[i].copy()
            backtest_result['available_fund'].iloc[i] = backtest_result['available_fund'].iloc[i - 1] - \
                                                        backtest_result['price'].iloc[i] * 100 * delta
            backtest_result['total_value'].iloc[i] = backtest_result['available_fund'].iloc[i] + \
                                                     backtest_result['security_amount'].iloc[i] * \
                                                     backtest_result['price'].iloc[i] * 100
        else:
            backtest_result['security_amount'].iloc[i] = backtest_result['security_amount'].iloc[i - 1].copy()
            backtest_result['last_trade_price'].iloc[i] = backtest_result['last_trade_price'].iloc[i - 1].copy()
            backtest_result['available_fund'].iloc[i] = backtest_result['available_fund'].iloc[i - 1].copy()
            backtest_result['total_value'].iloc[i] = backtest_result['available_fund'].iloc[i] + \
                                                     backtest_result['security_amount'].iloc[i] * \
                                                     backtest_result['price'].iloc[i] * 100

    return backtest_result
