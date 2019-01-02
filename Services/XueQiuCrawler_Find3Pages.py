import requests
import time
import re
from Services import Services


def crawler(page):
    url_base = 'https://xueqiu.com/'
    url_data = 'https://xueqiu.com/v4/statuses/user_timeline.json?page=%d&user_id=6042339231' % page
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'xueqiu.com',
        'Referer': 'https://xueqiu.com/u/6042339231',
        'Save-Data': 'on',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    s = requests.Session()
    s.headers.update(headers)  # Set Headers
    # With the url_base, the Session could get a Cookie
    s.get(url_base)
    r = s.get(url_data)
    user_data = r.json()
    user_post = user_data['statuses']
    return user_post


def post_manage(user_post, date_input):
    date = date_input
    for i in range(len(user_post)):
        post_time = time.localtime(user_post[i]['created_at']/1000)
        post_day = time.strftime("%Y%m%d", post_time)
        post_hour = time.strftime("%H", post_time)
        # Three Judgement: date matches, time matches, the beginning words match
        if date == post_day and int(post_hour) >= 15 and Services.weekday(date=date) in user_post[i]['text'][0:10]:
            today_post = user_post[i]['text']
            today_post_list = re.split(r"<p>|</p>|<br/>", today_post)
            while '' in today_post_list:
                today_post_list.remove('')
            today_post = ''
            for j in today_post_list:
                today_post = today_post + j
            return today_post


def get_comment(date):
    for page in range(3):
        user_post = crawler(page=page + 1)
        return post_manage(user_post, date_input=date)


if __name__ == "__main__":
    print(get_comment(date='20181221'))