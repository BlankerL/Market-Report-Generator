from Services import StockDetailFinder, DerivativeDetailFinder, Services


# The given id_dict should be like
# {'main': '', 'others':['',...,''],'index':''}
def market_overview(series_id_dict, date, series_name):
    # print date
    weekday = Services.weekday_printer(date=date)
    print(weekday, end='，')
    print(series_name, end='')

    # To deal with the 'main' in the dictionary given.
    print('主力合约', end='')
    sec_name, pct_chg, chg, close, open_interest, open_interest_chg, volume, spread = DerivativeDetailFinder.Session(series_id_dict['main'], date).data_printer()
    if pct_chg < 0:
        print('%s收盘跌%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close), end='，')
    elif pct_chg == 0:
        print('%s收盘报%.2f点，与开盘价格持平' % (sec_name, close), end='，')
    else:
        print('%s收盘涨%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close), end='，')

    if spread > 0:
        print('升水%.2f点' % (abs(spread)), end='。')
    elif spread == 0:
        print('与现券价格相等', end='。')
    else:
        print('贴水%.2f点' % (abs(spread)), end='。')

    volume = volume / 10000
    open_interest = open_interest / 10000
    if open_interest_chg > 0:
        print('全天成交%.2f万手，持仓%.2f万手，增仓%d手' % (volume, open_interest, abs(open_interest_chg)), end='。')
    elif open_interest_chg == 0:
        print('全天成交%.2f万手，持仓%.2f万手，增减仓%d手' % (volume, open_interest, abs(open_interest_chg)), end='。')
    else:
        print('全天成交%.2f万手，持仓%.2f万手，减仓%d手' % (volume, open_interest, abs(open_interest_chg)), end='。')

    # To deal with the 'others' in the dictionary given.
    print('其他合约方面', end='，')
    for id_num in range(len(series_id_dict['others'])):
        derivative_id = series_id_dict['others'][id_num]
        sec_name, pct_chg, chg, close, open_interest, open_interest_chg, volume, spread = DerivativeDetailFinder.Session(derivative_id, date).data_printer()
        if id_num < len(series_id_dict['others'])-1:
            symbol = '；'
        else:
            symbol = '。'
        if chg > 0:
            print('%s涨%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close), end=symbol)
        elif chg == 0:
            print('%s报%.2f点，与开盘价格持平' % (sec_name, close), end=symbol)
        else:
            print('%s跌%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close), end=symbol)

    # To deal with the 'index' in the dictionary given.
    print('现货方面', end='，')
    sec_name, pct_chg, chg, close, amt = StockDetailFinder.Session(series_id_dict['index'], date).data_printer()
    if chg > 0:
        print('%s指数收盘涨%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close), end='。\n')
    elif chg == 0:
        print('%s指数报%.2f点，与开盘价格持平' % (sec_name, close), end='。\n')
    else:
        print('%s指数收盘跌%.2f点或%.2f%%，报%.2f点' % (sec_name, abs(chg), abs(pct_chg), close), end='。\n')
