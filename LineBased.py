from WindPy import *
import datetime
import time
import sys
import Services
import Index_Overview
import Derivatives_Overview
import XueQiuSpider_Find3Pages


if __name__ == "__main__":

    w.start()

    DATE = input('请输入想要导出的日期（如20181030）：')
    weekday = datetime.datetime(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8])).weekday()
    if weekday == 5 or weekday == 6:
        print('日期不在周一至周五的范围内，程序即将结束。')
        time.sleep(2)
        sys.exit(0)
    else:
        pass

    print('全球市场')
    # Chinese Market
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    print(Index_Overview.overview_china(Stock_ID_List_CN, DATE), end='')
    # Asian Market
    Stock_ID_Asia = "N225.GI,KS11.GI,AS51.GI"
    Stock_ID_List_Asia = Stock_ID_Asia.split(',')
    print(Index_Overview.overview_others('亚太股市', Stock_ID_List_Asia, DATE))

    print('成交量')
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    print(Index_Overview.volume(Stock_ID_List_CN, DATE))

    print('宏观策略')
    XueQiuSpider_Find3Pages.get_comment(date=DATE)
    print('\n')

    # TODO: Bugs: 用涨跌来判断是否持平，而不应该用涨跌幅
    print('海外市场')

    # US Market
    # if int(datetime.datetime.today().strftime("%H")) <=  or int(datetime.datetime.today().strftime("%H")) >=
    Stock_ID_US = "DJI.GI,SPX.GI,IXIC.GI"
    Stock_ID_List_US = Stock_ID_US.split(',')
    print(Index_Overview.overview_others('美国三大股指', Stock_ID_List_US, DATE),end='')
    # European Market
    Stock_ID_US = "FTSE.GI,FCHI.GI,GDAXI.GI"
    Stock_ID_List_US = Stock_ID_US.split(',')
    print(Index_Overview.overview_others('欧洲三大股指', Stock_ID_List_US, DATE),end='')
    # Asian Market
    Stock_ID_Asia = "N225.GI,KS11.GI,AS51.GI"
    Stock_ID_List_Asia = Stock_ID_Asia.split(',')
    print(Index_Overview.overview_others('亚太股市', Stock_ID_List_Asia, DATE))

'''
    print('金融期货')
    # TODO: bugs to fix. 涨跌幅数据错误会导致数据导出有误。
    ID_Dictionary = Services.derivatives_getter()
    Derivatives_Overview.market_overview(ID_Dictionary['IH_Series'], DATE, '上证50股指期货')
    Derivatives_Overview.market_overview(ID_Dictionary['IC_Series'], DATE, '中证500股指期货')
    Derivatives_Overview.market_overview(ID_Dictionary['IF_Series'], DATE, '沪深300股指期货')
'''
    # TODO: add '国债期货' module.
    # TODO: user TKinter to make it visulized.