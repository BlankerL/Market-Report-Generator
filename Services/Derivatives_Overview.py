from WindPy import *
from Services import StockDetailFinder, DerivativeDetailFinder, Appendix


# The given id_dict should be like
# {'main': '', 'others':['',...,''],'index':''}
def market_overview(series_id_dict, date, series_name):
    output_string = ''
    # print date
    weekday = Appendix.weekday_printer(date=date)
    output_string = output_string + weekday + '，'
    output_string = output_string + series_name

    # To deal with the 'main' in the dictionary given.
    output_string = output_string + '主力合约'
    sec_name, pct_chg, chg, close, open_interest, open_interest_chg, volume, spread = DerivativeDetailFinder.Session(series_id_dict['main'], date).data_printer()
    if chg < 0:
        output_string = output_string + '%s收盘跌%.2f点或%.2f%%，报%.2f点，' % (sec_name, abs(chg), abs(pct_chg), close)
    elif chg == 0:
        output_string = output_string + '%s收盘报%.2f点，与开盘价格持平，' % (sec_name, close)
    else:
        output_string = output_string + '%s收盘涨%.2f点或%.2f%%，报%.2f点，' % (sec_name, abs(chg), abs(pct_chg), close)

    if spread > 0:
        output_string = output_string + '升水%.2f点。' % (abs(spread))
    elif spread == 0:
        output_string = output_string + '与现券价格相等。'
    else:
        output_string = output_string + '贴水%.2f点。' % (abs(spread))

    volume = volume / 10000
    open_interest = open_interest / 10000
    if open_interest_chg > 0:
        output_string = output_string + '全天成交%.2f万手，持仓%.2f万手，增仓%d手。' % (volume, open_interest, abs(open_interest_chg))
    elif open_interest_chg == 0:
        output_string = output_string + '全天成交%.2f万手，持仓%.2f万手，增减仓%d手。' % (volume, open_interest, abs(open_interest_chg))
    else:
        output_string = output_string + '全天成交%.2f万手，持仓%.2f万手，减仓%d手。' % (volume, open_interest, abs(open_interest_chg))

    # To deal with the 'others' in the dictionary given.
    output_string = output_string + '其他合约方面，'
    for id_num in range(len(series_id_dict['others'])):
        derivative_id = series_id_dict['others'][id_num]
        sec_name, pct_chg, chg, close, open_interest, open_interest_chg, volume, spread = DerivativeDetailFinder.Session(derivative_id, date).data_printer()
        if id_num < len(series_id_dict['others'])-1:
            symbol = '；'
        else:
            symbol = '。'
        if chg > 0:
            output_string = output_string + '%s涨%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close) + symbol
        elif chg == 0:
            output_string = output_string + '%s报%.2f点，与开盘价格持平' % (sec_name, close) + symbol
        else:
            output_string = output_string + '%s跌%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close) + symbol

    # To deal with the 'index' in the dictionary given.
    output_string = output_string + '现货方面，'
    sec_name, pct_chg, chg, close, amt = StockDetailFinder.Session(series_id_dict['index'], date).data_printer()
    if chg > 0:
        output_string = output_string + '%s指数收盘涨%.2f点或%.2f%%，报%.2f点。\n' % (sec_name, abs(chg), abs(pct_chg), close)
    elif chg == 0:
        output_string = output_string + '%s指数报%.2f点，与开盘价格持平。\n' % (sec_name, close)
    else:
        output_string = output_string + '%s指数收盘跌%.2f点或%.2f%%，报%.2f点。\n' % (sec_name, abs(chg), abs(pct_chg), close)

    return output_string


if __name__ == "__main__":
    w.start()
    print('金融期货')

    ID_Dictionary = Appendix.derivatives_getter()
    DATE = '20190102'
    market_overview(ID_Dictionary['IH_Series'], DATE, '上证50股指期货')
    market_overview(ID_Dictionary['IC_Series'], DATE, '中证500股指期货')
    market_overview(ID_Dictionary['IF_Series'], DATE, '沪深300股指期货')
