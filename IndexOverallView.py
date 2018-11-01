# -*- coding: utf-8 -*-
from WindPy import *
import time
import datetime


w.start()


class StockIdPrinter:
    def __init__(self, stock_id, date_input):
        self.stock_id = stock_id
        self.date_input = date_input

    def data_manage(self):
        get_data = w.wss(self.stock_id,
                         "SEC_NAME,WINDCODE,CHG,PCT_CHG,CLOSE3",
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
            round(data_dict[self.stock_id]['CHG'], 2), round(data_dict[self.stock_id]['CLOSE3'], 2)


def weekday_returner(date_input):
    weekday = datetime.datetime(int(date_input[0:4]), int(date_input[4:6]), int(date_input[6:8])).weekday()
    return {
        '0': '周一',
        '1': '周二',
        '2': '周三',
        '3': '周四',
        '4': '上周五'
    }.get(str(weekday))


def text_generator(stock_id_list, date):
    weekday = weekday_returner(date_input=date)
    date = date[4:6] + '月' + date[6:8] + '日'
    weekday = weekday + '（' + date + '）'
    print(weekday, end='，')

    for stock_num in range(len(stock_id_list)):
        stock = stock_id_list[stock_num]
        sec_name, pct_chg, chg, close = StockIdPrinter(stock, date).data_printer()
        if stock_num < len(stock_id_list)-1:
            symbol = '；'
        elif stock_num == len(stock_id_list)-1:
            symbol = '。'
        if pct_chg < 0:
            print('%s跌%.2f%%或%.2f点，报%.2f点' % (sec_name, abs(pct_chg), abs(chg), close), end=symbol)
        elif pct_chg == 0:
            print('%s报%.2f点，与开盘价格持平' % (sec_name, close), end=symbol)
        else:
            print('%s涨%.2f%%或%.2f点，报%.2f点' % (sec_name, abs(pct_chg), abs(chg), close), end=symbol)


if __name__ == "__main__":
    Stock_ID = input('请输入想要查询的股票代码，逗号隔开，默认主板指数请输入1：')
    DATE = input('请输入想要导出的日期（如20181030），默认为当天：')
    weekday = datetime.datetime(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8])).weekday()
    if weekday == 5 or weekday == 6:
        print('日期不在周一至周五的范围内，程序即将结束。')
        time.sleep(2)
        sys.exit(0)
    else:
        pass
    if Stock_ID != '1':  # If there is a string input
        pass
    elif Stock_ID == '1':
        Stock_ID = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List = Stock_ID.split(',')
    text_generator(Stock_ID_List, DATE)
