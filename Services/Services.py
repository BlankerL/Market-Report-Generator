import datetime
import requests


def date_optimizer(month_or_day):
    if month_or_day[0] == '0':
        return month_or_day[1]
    else:
        return month_or_day


def weekday(date):
    weekday = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])).weekday()
    return {
        '0': '周一',
        '1': '周二',
        '2': '周三',
        '3': '周四',
        '4': '周五'
    }.get(str(weekday))


def weekday_returner(date):
    weekday = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])).weekday()
    return {
        '0': '周一',
        '1': '周二',
        '2': '周三',
        '3': '周四',
        '4': '上周五'
    }.get(str(weekday))


def weekday_printer(date):
    weekday = weekday_returner(date=date)
    date = date_optimizer(date[4:6]) + '月' + date_optimizer(date[6:8]) + '日'
    return weekday + '（' + date + '）'


def derivatives_getter():
    url = 'https://BlankerL.github.io/UpdateChecker/Market_Report/derivatives.json'
    data = requests.get(url=url)
    return data.json()
