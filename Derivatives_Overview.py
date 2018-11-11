import DerivativeDetailFinder
import Services


def market_overview(id_dict, date):
    # print date
    weekday = Services.weekday_printer(date=date)
    print(weekday, end='，')
    sec_name, pct_chg, chg, close, amt = DerivativeDetailFinder.Session(id_dict['main'])

    # TODO: make it usable(used to be list type)
    for stock_num in range(len(id_dict)):
        stock = id_dict[stock_num]
        sec_name, pct_chg, chg, close, amt = DerivativeDetailFinder.Session(stock, date).data_printer()
        if stock_num < len(id_dict)-1:
            symbol = '；'
        else:
            symbol = '。\n'
        if pct_chg < 0:
            print('%s跌%.2f%%或%.2f点，报%.2f点' % (sec_name, abs(pct_chg), abs(chg), close), end=symbol)
        elif pct_chg == 0:
            print('%s报%.2f点，与开盘价格持平' % (sec_name, close), end=symbol)
        else:
            print('%s涨%.2f%%或%.2f点，报%.2f点' % (sec_name, abs(pct_chg), abs(chg), close), end=symbol)