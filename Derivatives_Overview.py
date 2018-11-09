import DerivativeDetailFinder
import Services


def market_overview(id_dict, date):
    # print date
    weekday = Services.weekday_printer(date=date)
    print(weekday, end='，')
    sec_name, pct_chg, chg, close, amt = DerivativeDetailFinder.Session(id_dict['main'])
