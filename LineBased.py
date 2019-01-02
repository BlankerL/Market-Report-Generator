from WindPy import *
import datetime
import time
import sys
from Services import Index_Overview, XueQiuCrawler_Find3Pages, Appendix, Derivatives_Overview

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
    # US Market
    # if int(datetime.datetime.today().strftime("%H")) <=  or int(datetime.datetime.today().strftime("%H")) >=
    Stock_ID_US = "DJI.GI,SPX.GI,IXIC.GI"
    Stock_ID_List_US = Stock_ID_US.split(',')
    print(Index_Overview.overview_others('美国三大股指', Stock_ID_List_US, DATE), end='')
    # European Market
    Stock_ID_EU = "FTSE.GI,FCHI.GI,GDAXI.GI"
    Stock_ID_List_EU = Stock_ID_EU.split(',')
    print(Index_Overview.overview_others('欧洲三大股指', Stock_ID_List_EU, DATE), end='')
    # Asian Market
    Stock_ID_Asia = "N225.GI,KS11.GI,AS51.GI"
    Stock_ID_List_Asia = Stock_ID_Asia.split(',')
    print(Index_Overview.overview_others('亚太股市', Stock_ID_List_Asia, DATE))

    print('成交量')
    Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
    Stock_ID_List_CN = Stock_ID_CN.split(',')
    print(Index_Overview.volume(Stock_ID_List_CN, DATE), end='\n\n')

    print('宏观策略')
    print(XueQiuCrawler_Find3Pages.get_comment(date=DATE), end='\n\n')

    print('金融期货')
    ID_Dictionary = Appendix.derivatives_getter()
    print(Derivatives_Overview.market_overview(ID_Dictionary['IH_Series'], DATE, '上证50股指期货'), end='')
    print(Derivatives_Overview.market_overview(ID_Dictionary['IC_Series'], DATE, '中证500股指期货'), end='')
    print(Derivatives_Overview.market_overview(ID_Dictionary['IF_Series'], DATE, '沪深300股指期货'), end='')

    # TODO: add '国债期货' module.
