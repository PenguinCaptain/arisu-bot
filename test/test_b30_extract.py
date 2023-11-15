import requests
from bs4 import BeautifulSoup
import json

# 获取cookies
account = "acekuro0219"
password = "gzycTaffyxxm0915"
login_url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=chuniex&redirect_url=https://chunithm-net-eng.com/mobile/&back_url=https://chunithm.sega.com/'
response_login = requests.get(login_url)
cookies_login = response_login.headers['Set-Cookie']

# 尝试登录 + 重新定向到chunithm-net网站
login_page = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid/'
response_redirect = requests.post(login_page, headers={'cookie': cookies_login}, data={
    'retention': 1, 'sid': account, 'password': password}, allow_redirects=False)

redirect_page = response_redirect.headers['location']
cookies_redirect = response_redirect.cookies

response = requests.get(redirect_page, cookies=cookies_redirect)

player_data = response.text


soup = BeautifulSoup(player_data, 'html.parser')

soup_data = soup.find(id="inner").find("div", {"class": "player_data_right"})

open("best30_playerData.html", "w").write(str(soup_data))

# 从这里开始复制回去