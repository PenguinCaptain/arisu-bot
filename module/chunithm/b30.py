import requests
from bs4 import BeautifulSoup
import json
import time
from module.chunithm.calc import score_to_rating
from PIL import Image, ImageDraw, ImageFont
from aiocqhttp.message import MessageSegment
import base64

# 获取cookies
def generate_b30(account, password):
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
        return "Error: Account or Password is invalid. Please Try Again."
    else:
        print('Get userId successfully.')

    # 获取 player_data


    soup = BeautifulSoup(player_data, 'html.parser')

    soup = soup.find(id="inner").find("div", {"class": "player_data_right"})

    try:
        team = soup.find("div", {"class": "player_team_data"}).div.string
    except:
        team = ""
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

    data_chunirec = json.loads(open("./module/chunithm/data/data_chunirec.json").read())

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
            "const": const,
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
            "const": const,
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

    b30make(player_data)

    token = "6d207e02198a847aa98d0a2a901485a5"

    url = "https://freeimage.host/api/1/upload"

    

    content = open("./src/res.png", "rb").read()

    
    # base64.b64encode(content)

    request = requests.post(url, {
        "key": token,
        "action": "upload",
        "image": base64.b64encode(content),
        "format": "json"
    })

    # request.json()["data"]["display_url"]

    url = request.json()["image"]["url"]

    
    

    return MessageSegment.image(url)

# # 作为export的接口
# open("./best30.reiwa5.json", "w").write(json.dumps(player_data, ensure_ascii=False))

def fth(s):
    s1 = ""
    for uchar in s:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
            inside_code = uchar
        else:
            inside_code = chr(inside_code)
        s1 += inside_code
    return s1
    

def b30make(data):
    """
    "team": "Ｉｔ　Ｉｓ・Ｄｏｇｓｈｏｕｔ　ＴＩＭＥ！",
    "honor": "NEW COMER",
    "name": "ｋｌｑｉｅＦａｎ",
    "rating": 16.52,
    "ratingMax": 16.53,
    "updatedAt": "2023-11-16T20:06:29+08:00",
    """

    base = Image.open("./src/chunithm/blue.PNG").resize((1800, 2050))

    ico = Image.open("./src/chunithm/ico.png").convert("RGBA")

    final_ico = Image.new("RGBA", ico.size, color=(255, 255, 255))

    final_ico = Image.alpha_composite(final_ico, ico)

    final_ico = final_ico.resize((180, 180))

    base.paste(final_ico, (60, 40))


    draw = ImageDraw.Draw(base)

    font = ImageFont.truetype("./src/chunithm/font/BAHNSCHRIFT.ttf", 80)
    font_2 = ImageFont.truetype("./src/chunithm/font/BAHNSCHRIFT.ttf", 40)
    font_3 = ImageFont.truetype("./src/chunithm/font/BAHNSCHRIFT.ttf", 22)
    draw.polygon([(340, 40), (280, 220), (1700, 220), (1760, 40)], fill=(255, 255, 255))
    draw.text((380, 60), "Player name:", (0, 0, 0), font_2)
    draw.text((380, 110), fth(data["name"]), (0, 0, 0), font)

    draw.text((1050, 60), f"Rating: {data['rating']}", (0, 0, 0), font)
    draw.text((1500, 90), f"/Max: {data['ratingMax']}", (0, 0, 0), font_2)

    draw.text((1050, 160), f"Best30: {round(data['best30'], 4)} / Recent10: {round(data['recent10'], 4)}", (0, 0, 0), font_2)

    draw.line([(10, 270), (580, 270)], fill=(255, 255, 255), width=10)

    draw.text((590, 251), "Best", (255, 255, 255), font_2)

    draw.line([(680, 270), (1490, 270)], fill=(255, 255, 255), width=10)

    draw.text((1500, 251), "Recent", (255, 255, 255), font_2)

    draw.line([(1630, 270), (1790, 270)], fill=(255, 255, 255), width=10)

    draw.line([(1324, 270), (1324, 1990)], fill=(255, 255, 255), width=10)

    draw.text((1550, 2000), f"Generated by Arisu_Bot\nDesigned by Kuroko", (0, 0, 0), font_3)

    count = 0

    for song in data["best"]:
        pic = b30single(song, count + 1)
        base.paste(pic, (20 + count % 3 * 430, 310 + count // 3 * 168))
        count += 1
    
    count = 0

    for song in data["recent"]:
        pic = b30single(song, count + 1)
        base.paste(pic, (1350, 310 + count * 168))
        count += 1
    
    base.save("./src/res.png")

def b30single(data, count):
    color = {
        'Master': (187, 51, 238),
        'Expert': (238, 67, 102),
        'Advanced': (254, 170, 0),
        'Ultima': (0, 0, 0),
        'Basic': (102, 221, 17),
    }

    """
    "title": "Giselle",
    "score": 1007542,
    "difficulty": "Master",
    "id": "c893",
    "const": 14.9,
    "rating": 16.9,
    "token": "99c5e71073e0f616327cf3c490ba2a05",
    "isAllJustice": false,
    "isFullCombo": false
    """
    title = data["title"]
    score = data["score"]
    diff = data["difficulty"]
    rating = data["rating"]
    const = data["const"]
    id = data["id"]
    

    base = Image.new("RGBA", (620, 240), (255, 255, 255, 175))
    
    jacket = Image.open(f'./module/chunithm/image/{id}.jpg')
    jacket = jacket.resize((186, 186))
    base.paste(jacket, (32, 28))

    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype('./src/chunithm/font/NotoSansHans-Regular-2.ttf', 37)
    size = font.getlength(title)
    if size > 345:
        title = title[:int(len(title)*(345/size))]
    draw.text((270, 38), title, '#000000', font)

    font_2 = ImageFont.truetype('./src/chunithm/font/BAHNSCHRIFT.TTF', 58)
    draw.text((240, 107), str(score), '#000000', font_2)

    font_4 = ImageFont.truetype('./src/chunithm/font/BAHNSCHRIFT.TTF', 29)
    draw.text((540, 135), f"(#{count})", '#000000', font_4)

    font_3 = ImageFont.truetype('./src/chunithm/font/BAHNSCHRIFT.TTF', 42)
    draw.rectangle((240, 27, 255, 87), fill=color[diff])
    draw.text((240, 177), "Rating: " + str(const) + '  >  ' + str(rating), (0, 0, 0), font_3)

    # 280 105

    base = base.resize((420, 158))
    return base