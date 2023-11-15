import requests
from bs4 import BeautifulSoup
import json
import time

# # 获取cookies
# account = "acekuro0219"
# password = "gzycTaffyxxm0915"
# login_url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=chuniex&redirect_url=https://chunithm-net-eng.com/mobile/&back_url=https://chunithm.sega.com/'
# response_login = requests.get(login_url)
# cookies_login = response_login.headers['Set-Cookie']

# # 尝试登录 + 重新定向到chunithm-net网站
# login_page = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid/'
# response_redirect = requests.post(login_page, headers={'cookie': cookies_login}, data={
#     'retention': 1, 'sid': account, 'password': password}, allow_redirects=False)

# redirect_page = response_redirect.headers['location']
# cookies_redirect = response_redirect.cookies

# response = requests.get(redirect_page, cookies=cookies_redirect)

# player_data = response.text
# soup = BeautifulSoup(player_data, 'html.parser')
# soup_data = soup.find(id="inner").find("div", {"class": "player_data_right"})
# open("best30_playerData.html", "w").write(str(soup_data))

# 从这里开始复制回去

player_data = open("./best30_playerData.html").read()
soup = BeautifulSoup(player_data, 'html.parser')
# soup_data = soup.find(id="inner").find("div", {"class": "player_data_right"})

team = soup.find("div", {"class": "player_team_data"}).div.string
honor = soup.find("div", {"class": "player_honor_short"}).div.div.span.string
player_name_soup = soup.find("div", {"class": "player_name"}).find_all("div")
player_level = player_name_soup[0].string
player_name = player_name_soup[1].string
player_rating_max = soup.find("div", {"class": "player_rating_max"}).string
del player_name_soup


update_time = time.strftime(r"%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time()))

