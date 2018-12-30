# -*- coding: utf-8 -*-
import StockDetailFinder
import Services
from WindPy import *


# The main difference between China and Others are the delivery of contents.
# In China, I need to mention the specific points of going up or down.
# In other markets, it is in no need. But I need to mention all the N markets total performance.
def overview_china(stock_id_list, date):
    output_string = ''
    # print date
    weekday = Services.weekday_printer(date=date)
    output_string = output_string + weekday + '，'

    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        sec_name, pct_chg, chg, close, amt = StockDetailFinder.Session(stock, date).data_printer()
        # Symbol Generator
        if stock_num < len(stock_id_list)-1:
            symbol = '；'
        else:
            symbol = '。\n'

        if pct_chg < 0:
            output_string = output_string + '{sec_name}跌{pct_chg:.2f}%或{chg:.2f}点，报{close:.2f}点'.format(
                sec_name=sec_name, pct_chg=abs(pct_chg), chg=abs(chg), close=close) + symbol
        elif pct_chg == 0:
            output_string = output_string + '{sec_name}报{close:.2f}点，与开盘价格持平'.format(
                sec_name=sec_name, close=close) + symbol
        else:
            output_string = output_string + '{sec_name}涨{pct_chg:.2f}%或{chg:.2f}点，报{close:.2f}点'.format(
                sec_name=sec_name, pct_chg=abs(pct_chg), chg=abs(chg), close=close) + symbol

    return output_string


def overview_others(market_type, stock_id_list, date):
    output_string = ''
    # print date
    weekday = Services.weekday_printer(date=date)
    output_string = output_string + weekday + '，'
    # parameters for save data into dict and generate the overview words of the market
    go_up = 0
    stock_dict = {}
    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        stock_dict[stock_num] = {}
        stock_dict[stock_num]['sec_name'], stock_dict[stock_num]['pct_chg'], stock_dict[stock_num]['chg'], stock_dict[stock_num]['close'], stock_dict[stock_num]['amt'] = StockDetailFinder.Session(stock, date).data_printer()
    for stock_num in range(len(stock_id_list)):
        if stock_dict[stock_num]['pct_chg'] > 0:
            go_up = go_up + 1
        else:
            pass
    output_string = output_string + market_type
    if go_up == len(stock_id_list):
        output_string = output_string + '收盘全线上涨。'
    elif go_up >= len(stock_id_list)/2:
        output_string = output_string + '收盘普涨。'
    elif go_up < len(stock_id_list)/2:
        output_string = output_string + '收盘普跌。'
    elif go_up == 0:
        output_string = output_string + '收盘全线下跌。'
    # read data in the dict and print the performance of the market of the day
    for stock_num in range(len(stock_id_list)):
        stock_dict[stock_num]['sec_name'] = {
            '日经225': '日经225指数',
            '韩国综合指数': '韩国综合指数',
            '澳洲标普200': '澳大利亚ASX200指数',
            '道琼斯工业指数': '道琼斯工业平均指',
            '标普500': '标普500指数',
            '纳斯达克指数': '纳斯达克综合指数',
            '富时100': '英国富时100指数',
            '法国CAC40': '法国CAC40指数',
            '德国DAX': '德国DAX指数'
        }.get(stock_dict[stock_num]['sec_name'], 'Error!')
        if stock_num < len(stock_id_list) - 1:
            symbol = '；'
        else:
            symbol = '。\n'
        if stock_dict[stock_num]['pct_chg'] < 0:
            output_string = output_string + '{sec_name}跌{pct_chg:.2f}%，报{close}点'.format(
                sec_name=stock_dict[stock_num]['sec_name'], pct_chg=abs(stock_dict[stock_num]['pct_chg']), close=stock_dict[stock_num]['close']) + symbol
        elif stock_dict[stock_num]['pct_chg'] == 0:
            output_string = output_string + '{sec_name}报{close}点，与开盘价格持平'.format(
                sec_name=stock_dict[stock_num]['sec_name'], close=stock_dict[stock_num]['close']) + symbol
        else:
            output_string = output_string + '{sec_name}涨{pct_chg:.2f}%，报{close}点'.format(
                sec_name=stock_dict[stock_num]['sec_name'], pct_chg=abs(stock_dict[stock_num]['pct_chg']), close=stock_dict[stock_num]['close']) + symbol

    return output_string


def volume(stock_id_list, date):
    output_string = ''
    output_string = output_string + "成交量方面，"
    total_amt_today = 0
    total_amt_yesterday = 0
    # Today Volume
    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        sec_name, pct_chg, chg, close, amt = StockDetailFinder.Session(stock, date).data_printer()
        sec_name = {
            '上证综指': '沪市',
            '深证成指': '深市',
            '创业板指': '创业板'
        }.get(sec_name, 'Error!')
        amt = amt/100000000
        output_string = output_string + '{sec_name}成交{amt:.2f}亿元'.format(
            sec_name=sec_name, amt=amt) + '，'
        total_amt_today = total_amt_today + amt
    # Yesterday Volume
    if Services.weekday_returner(date) == '周一':  # TODO: BUGS: 注意节假日避让
        yesterday_date = str(int(date)-3)
    else:
        yesterday_date = str(int(date)-1)
    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        sec_name, pct_chg, chg, close, amt = StockDetailFinder.Session(stock, yesterday_date).data_printer()
        amt = amt / 100000000
        total_amt_yesterday = total_amt_yesterday + amt
    output_string = output_string + '总成交额{total_amt_today:.2f}亿元'.format(
        total_amt_today=total_amt_today) + '，'
    if total_amt_today > total_amt_yesterday * 1.2:
        output_string = output_string + '较上一交易日量能明显上升。'
    elif total_amt_yesterday < total_amt_today < total_amt_yesterday * 1.2:
        output_string = output_string + '较上一交易日有所上升。'
    elif total_amt_today < total_amt_yesterday * 0.8:
        output_string = output_string + '较上一交易日成交量显著减小。'
    elif total_amt_today < total_amt_yesterday:
        output_string = output_string + '较上一交易日成交量有所缩小。'

    return output_string


if __name__ == "__main__":
    w.start()

    print('全球市场')
    # Chinese Market
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    print(overview_china(Stock_ID_List_CN, '20181221'), end='')
    # Asian Market
    Stock_ID_Asia = "N225.GI,KS11.GI,AS51.GI"
    Stock_ID_List_Asia = Stock_ID_Asia.split(',')
    print(overview_others('亚太股市', Stock_ID_List_Asia, '20181221'))

    print('成交量')
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    print(volume(Stock_ID_List_CN, '20181221'))