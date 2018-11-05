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
        'Cookie': 'aliyungf_tc=AQAAALeZfgKujQsAk/SUPfNQv2CAZWzh; xq_a_token=088c6ad5e275496d7c91b8b5b2ecb929bee15772; xq_a_token.sig=NcpAm7FRsAVoMGRMOLrLRveBT7U; xq_r_token=08131eb9a4f33b43b2340fd782f3776c9823d74a; xq_r_token.sig=AZ7au6ICJtTgQJVPybkOJs_Fr54; u=311541140095545; _ga=GA1.2.203920210.1541140096; _gid=GA1.2.21779304.1541140096; device_id=487215c08fc95cae2b41a9b9e9d3737a; Hm_lvt_1db88642e346389874251b5a1eded6e3=1541140097; s=f616a40kh5; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1541140102; _gat_gtag_UA_16079156_4=1',
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
    year = time.strftime("%Y", time.localtime())
    date = date_input
    for i in range(len(user_post)):
        post_time = time.localtime(user_post[0]['created_at']/1000)
        post_day = time.strftime("%Y%m%d", post_time)
        if date == post_day and Services.weekday_returner(date=date) in user_post[i]['text'][0:10]:
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
