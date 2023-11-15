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

response = requests.get(redirect_page, cookies=cookies_redirect, allow_redirects=False)

player_data = response.text

soup = BeautifulSoup(player_data, 'html.parser')

soup_form = soup.find(id="inner").find("div", {"class": "player_data_right"}).find_all("form")

# #inner > div.frame01.w460 > div.frame01_inside > div.mt_10 > div.box_playerprofile.\.clearfix > div.player_data_right

cookies = response.cookies

"""
cookies示例:
<RequestsCookieJar[<Cookie _t=d0530846ec80a8648e79153eea6f7e55 for chunithm-net-eng.com/>, <Cookie userId=4445256934383693 for chunithm-net-eng.com/>, <Cookie friendCodeList=8043676931841%2C5060426495140%2C9052547973349 for chunithm-net-eng.com/>]>
"""

userID = cookies["userId"] # 获取userID

# 如果"_t"不在cookies内 -> 登录失败，或许是账号/密码错误

if '_t' not in cookies:
    print("Account or Password is invalid. Please Try Again.")
else:
    print('Get userId successfully.')

# 获取Best30的html

best30_page = "https://chunithm-net-eng.com/mobile/home/playerData/ratingDetailBest/"
response_best = requests.get(best30_page, cookies=cookies)

# 调试用
# open(f"./best30_{userID}.html", "w").write(response_best.text)

# 解析Best30 html

content = response_best.text

soup = BeautifulSoup(content, 'html.parser')

soup_form = soup.find(id="inner").find("div", {"class": "box05 w400"}).find_all("form")

song_data = []

replace = {"0": "Basic", "1": "Advance", "2": "Expert", "3": "Master", "4": "Ultima"}

for soup_best in soup_form:
    data_div = soup_best.div.find_all("div")
    data_input = soup_best.div.find_all("input")
    song_data.append({
        "title": data_div[0].string,
        "score": int(data_div[1].span.string.replace(",","")),
        "difficulty": replace[data_input[0]["value"]],
        "id": "c" + data_input[2]["value"],
        "token": data_input[3]["value"],
        "isAllJustice": False,
        "isFullCombo": False
    })


# print(data.find("div", {"class": "music_title"}))


# open("./best30_extract.html", "w").write(str(soup_form))

open("./best30.preview.json", "w").write(json.dumps(song_data))

player_data = {
    "honor": "NEW COMER",
    "name": "klqieFan",
    "rating": 16.46,
    "ratingMax": 16.53,
    "updatedAt": "2023-11-09T18:09:02+08:00",
    "best": song_data,
    "recent": [],
    "candicate": []
}

open("./best30.reiwa5.json", "w").write(json.dumps(player_data, ensure_ascii=False))


