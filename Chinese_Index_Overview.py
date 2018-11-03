# -*- coding: utf-8 -*-
from WindPy import *
import Services

w.start()


class StockDetailFinder:
    def __init__(self, stock_id, date_input):
        self.stock_id = stock_id
        self.date_input = date_input

    def data_manage(self):
        get_data = w.wss(self.stock_id,
                         "SEC_NAME,WINDCODE,CHG,PCT_CHG,CLOSE3,AMT",
                         "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
        data_dict = {}
        for i in range(len(get_data.Codes)):
            codes = get_data.Codes[i]
            data_dict[codes] = {}
            for j in range(len(get_data.Fields)):
                data_name = get_data.Fields[j]
                data_dict[codes][data_name] = get_data.Data[j][i]
        return data_dict

    def data_printer(self):
        data_dict = self.data_manage()
        return data_dict[self.stock_id]['SEC_NAME'], round(data_dict[self.stock_id]['PCT_CHG'], 2), \
            round(data_dict[self.stock_id]['CHG'], 2), round(data_dict[self.stock_id]['CLOSE3'], 2), \
            data_dict[self.stock_id]['AMT']


def market_overview(stock_id_list, date):
    weekday = Services.weekday_returner(date=date)
    date = date[4:6] + '月' + date[6:8] + '日'
    weekday = weekday + '（' + date + '）'
    print(weekday, end='，')

    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        sec_name, pct_chg, chg, close, amt = StockDetailFinder(stock, date).data_printer()
        if stock_num < len(stock_id_list)-1:
            symbol = '；'
        else:
            symbol = '。\n'
        if pct_chg < 0:
            print('%s跌%.2f%%或%.2f点，报%.2f点' % (sec_name, abs(pct_chg), abs(chg), close), end=symbol)
        elif pct_chg == 0:
            print('%s报%.2f点，与开盘价格持平' % (sec_name, close), end=symbol)
        else:
            print('%s涨%.2f%%或%.2f点，报%.2f点' % (sec_name, abs(pct_chg), abs(chg), close), end=symbol)


def volume_detector(stock_id_list, date):
    print("成交量方面，", end='')
    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        sec_name, pct_chg, chg, close, amt = StockDetailFinder(stock, date).data_printer()
        if stock_num < len(stock_id_list)-1:
            symbol = '，'
        else:
            symbol = '。\n'
        sec_name = {
            '上证综指': '沪市',
            '深证成指': '深市',
            '创业板指': '创业板'
        }.get(sec_name, 'Error!')
        print('%s成交%.2f亿元' % (sec_name, (amt/100000000)), end=symbol)
