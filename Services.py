import datetime


def weekday_returner(date):
    weekday = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8])).weekday()
    return {
        '0': '周一',
        '1': '周二',
        '2': '周三',
        '3': '周四',
        '4': '上周五'
    }.get(str(weekday))