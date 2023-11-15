import requests
from bs4 import BeautifulSoup
import json
import time
from calc_score import score_to_rating

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


response = requests.get(redirect_page, cookies=cookies_redirect, allow_redirects=False) # 获取cookies
# 如果"_t"不在cookies内 -> 登录失败，或许是账号/密码错误
cookies = response.cookies

if '_t' not in cookies:
    print("Account or Password is invalid. Please Try Again.")
else:
    print('Get userId successfully.')

# 获取 player_data


soup = BeautifulSoup(player_data, 'html.parser')

soup = soup.find(id="inner").find("div", {"class": "player_data_right"})

team = soup.find("div", {"class": "player_team_data"}).div.string
honor = soup.find("div", {"class": "player_honor_short"}).div.div.span.string
player_name_soup = soup.find("div", {"class": "player_name"}).find_all("div")
player_level = player_name_soup[0].string
player_name = player_name_soup[1].string
player_rating_max = float(soup.find("div", {"class": "player_rating_max"}).string)
del player_name_soup


update_time = time.strftime(r"%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time()))

# open("best30_playerData.html", "w").write(str(soup_data))

# #inner > div.frame01.w460 > div.frame01_inside > div.mt_10 > div.box_playerprofile.\.clearfix > div.player_data_right


"""
cookies示例:
<RequestsCookieJar[<Cookie _t=d0530846ec80a8648e79153eea6f7e55 for chunithm-net-eng.com/>, <Cookie userId=4445256934383693 for chunithm-net-eng.com/>, <Cookie friendCodeList=8043676931841%2C5060426495140%2C9052547973349 for chunithm-net-eng.com/>]>
"""


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
replace_calc = {"0": "BAS", "1": "ADV", "2": "EXP", "3": "MAS", "4": "ULT"}

data_chunirec = json.loads(open("./data_chunirec.json").read())

best_30 = 0

for soup_best in soup_form:
    data_div = soup_best.div.find_all("div")
    data_input = soup_best.div.find_all("input")
    id = "c" + data_input[2]["value"]
    score = int(data_div[1].span.string.replace(",",""))
    diff = replace_calc[data_input[0]["value"]]
    const = data_chunirec[id]["data"][diff]["const"]
    song_data.append({
        "title": data_div[0].string,
        "score": int(data_div[1].span.string.replace(",","")),
        "difficulty": replace[data_input[0]["value"]],
        "id": "c" + data_input[2]["value"],
        "rating": score_to_rating(score, const),
        "token": data_input[3]["value"],
        "isAllJustice": False,
        "isFullCombo": False
    })
    best_30 += score_to_rating(score, const)

recent10_page = "https://chunithm-net-eng.com/mobile/home/playerData/ratingDetailRecent/"
response_recent = requests.get(recent10_page, cookies=cookies)

content = response_recent.text
soup = BeautifulSoup(content, 'html.parser')
soup_form = soup.find(id="inner").find("div", {"class": "box05 w400"}).find_all("form")

song_data_recent = []
replace = {"0": "Basic", "1": "Advance", "2": "Expert", "3": "Master", "4": "Ultima"}

recent_10 = 0

for soup_best in soup_form:
    data_div = soup_best.div.find_all("div")
    data_input = soup_best.div.find_all("input")
    id = "c" + data_input[2]["value"]
    score = int(data_div[1].span.string.replace(",",""))
    diff = replace_calc[data_input[0]["value"]]
    const = data_chunirec[id]["data"][diff]["const"]
    song_data_recent.append({
        "title": data_div[0].string,
        "score": int(data_div[1].span.string.replace(",","")),
        "difficulty": replace[data_input[0]["value"]],
        "id": "c" + data_input[2]["value"],
        "rating": score_to_rating(score, const),
        "token": data_input[3]["value"],
        "isAllJustice": False,
        "isFullCombo": False
    })
    recent_10 += score_to_rating(score, const)

# print(data.find("div", {"class": "music_title"}))


# open("./best30_extract.html", "w").write(str(soup_form))

# open("./best30.preview.json", "w").write(json.dumps(song_data))

player_data = {
    "team": team,
    "honor": honor,
    "name": player_name,
    "rating": round((best_30 + recent_10) / 40, 2),
    "ratingMax": player_rating_max,
    "updatedAt": update_time,
    "best": song_data,
    "recent": song_data_recent,
    "best30": best_30 / 30,
    "recent10": recent_10 / 10,
    "candicate": []
}

# 作为export的接口
open("./best30.reiwa5.json", "w").write(json.dumps(player_data, ensure_ascii=False))


