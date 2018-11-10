import requests
import time
import re
import Services


def spider(page):
    url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page=%d&user_id=6042339231' % page
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'device_id=9172e248317b67748470c7a69d133999; _ga=GA1.2.1523845760.1541414618; s=e412bj11pn; __utma=1.1523845760.1541414618.1541414655.1541414655.1; __utmz=1.1541414655.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_token_expire=Fri%20Nov%2030%202028%2018%3A49%3A45%20GMT%2B0800%20(CST); bid=9eef04913fa6855058bcf34246b845a7_jo46shnp; aliyungf_tc=AQAAAMvu6m8hjg0A6xFAfMavfh8atP/T; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1541414616,1541678339,1541851653; _gid=GA1.2.1023048645.1541851653; _gat_gtag_UA_16079156_4=1; xq_a_token=2da5342ee6de7bf35ff52ec296426e9c9670f647; xq_a_token.sig=C57MGRXU_-qi2-KXnJaQ6tX4qLI; xq_r_token=f37df9336ae424cffdbe3a31123f2ab4676ba00c; xq_r_token.sig=_VMY0dRhVuU359Ecmhs_1Gtuzto; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1541851675; u=511541851675239',
        'Host': 'xueqiu.com',
        'Referer': 'https://xueqiu.com/u/6042339231',
        'Save-Data': 'on',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    user_data = requests.get(url=url, headers=headers, timeout=3).json()
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
            for j in today_post_list:
                print(j)


def get_comment(date):
    for page in range(3):
        user_post = spider(page=page+1)
        post_manage(user_post, date_input=date)
