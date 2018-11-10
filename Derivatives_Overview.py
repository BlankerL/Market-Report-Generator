import StockDetailFinder
import Services

def market_overview(id_list, date):
    # print date
    weekday = Services.weekday_printer(date=date)
    print(weekday, end='，')