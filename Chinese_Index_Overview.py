# -*- coding: utf-8 -*-
from WindPy import *
import time
import datetime
import Services
import spider_Findtoday

w.start()


class StockIdPrinter:
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
        sec_name, pct_chg, chg, close, amt = StockIdPrinter(stock, date).data_printer()
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
        sec_name, pct_chg, chg, close, amt = StockIdPrinter(stock, date).data_printer()
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


if __name__ == "__main__":
    DATE = input('请输入想要导出的日期（如20181030）：')
    weekday = datetime.datetime(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8])).weekday()
    if weekday == 5 or weekday == 6:
        print('日期不在周一至周五的范围内，程序即将结束。')
        time.sleep(2)
        sys.exit(0)
    else:
        pass

    print('全球市场')
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    market_overview(Stock_ID_List_CN, DATE)
    Stock_ID_Asia = "N225.GI,KS11.GI,AS51.GI"
    Stock_ID_List_Asia = Stock_ID_Asia.split(',')
    market_overview(Stock_ID_List_Asia, DATE)

    print('\n成交量')
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    volume_detector(Stock_ID_List_CN, DATE)

    print('\n宏观策略')
    spider_Findtoday.get_comment(date=DATE)
