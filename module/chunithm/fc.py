import requests
import json
from http.cookiejar import CookiePolicy
from module.chunithm.calc import song_to_rating
from lxml import html

account = "acekuro0219"
password = "gzycTaffyxxm0915"

class CustomCookiePolicy(CookiePolicy):
    def set_ok(self, cookie, _):
        if cookie.name == "friendCodeList":
            return True
        return False

    return_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False

    netscape = True
    rfc2965 = hide_cookie2 = False


def generate_data(code):
    login_url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=chuniex&redirect_url=https://chunithm-net-eng.com/mobile/&back_url=https://chunithm.sega.com/'
    response_login = requests.get(login_url)
    cookies_login = response_login.headers['Set-Cookie']

    # 尝试登录 + 重新定向到chunithm-net网站
    login_page = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid/'
    response_redirect = requests.post(login_page, headers={'cookie': cookies_login}, data={
        'retention': 1, 'sid': account, 'password': password}, allow_redirects=False)
    redirect_page = response_redirect.headers['location']
    cookies_redirect = response_redirect.cookies


    response = requests.get(redirect_page, cookies=cookies_redirect, allow_redirects=False) # 获取cookies
    # 如果"_t"不在cookies内 -> 登录失败，或许是账号/密码错误
    cookies = response.cookies

    if '_t' not in cookies:
        return "Error: Account or Password is invalid. Please Try Again."
    else:
        print('Get userId successfully.')
    
    session = requests.Session()
    session.cookies.update({"userId": cookies["userId"], "_t": cookies["_t"]})
    session.cookies.set_policy(CustomCookiePolicy())

    print("Fetching friend list...")
    friend_list = get_friend_list(session)

    if code not in friend_list:
        invite_friend(session, code)
        print("Not a friend, invite sent")
        return

    print("Registering as favorite...")
    register_favorite(session, code)

    print("Fetching record...")
    url = "https://chunithm-net-eng.com/mobile/friend/genreVs/sendBattleStart/"
    record = []

    best30 = 0
    for i in range(4):
        response = session.post(
            url,
            data={
                "genre": "99",
                "friend": code,
                "radio_diff": str(i),
                "token": cookies["_t"],
            },
        )

        tree = html.fromstring(response.text)

        player_name = tree.xpath('//*[@id="inner"]/div[3]/div[2]/div[3]/form/div[1]/select[2]/option/text()')[0]

        music_boxes = tree.xpath('//div[contains(@class, "music_box")]')

        print(player_name, type(player_name))

        
        count = 30

        if not music_boxes:
            raise Exception("No songs available")
        for music_box in music_boxes:
            score = music_box.xpath(
                './/div[@class="vs_list_infoblock"][2]/div[1]/text()'
            )[0]
            if score == "0":
                continue
            music_name = music_box.xpath(
                './/div[@class="block_underline text_b text_c"]/div[1]/text()'
            )[0]
            fcaj_img = music_box.xpath(
                './/div[@class="vs_list_infoblock"][2]/div[2]/img/@src'
            )
            fcaj_img = fcaj_img[0] if fcaj_img else ""
            isAJ = "icon_alljustice" in fcaj_img
            isFC = "icon_fullcombo" in fcaj_img or isAJ

            score = int(score.replace(",", ""))
            
            rating, const = song_to_rating(music_name, diff_to_chunirec[str(i)], score)

            if count > 0:
                count -= 1
            try:
                id = data_chunirec_index[song_to_id[music_name]["meta"]["id"]]
            except:
                id = "c0"
            record.append(
                {
                    "title": music_name,
                    "difficulty": get_difficulty(str(i)),
                    "score": score,
                    "const": const,
                    "rating": rating,
                    "is_fc": isFC,
                    "is_aj": isAJ,
                    "id": id
                }
            )
        record = sorted(record, key=lambda x: (x["rating"]), reverse=True)
    for rec in record[:30]:
        best30 += rec["rating"]


    data = {
        "name": player_name,
        "rating": "--",
        "ratingMax": "--",
        "best": record,
        "best30": best30
    }

    print("Saving record...")
    # with open("best30.fetchByFrdCode.json", "w") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)
    return data

song_to_id = json.loads(open("./module/chunithm/data/data_song_to_const.json").read())
data_chunirec_index = json.loads(open("./module/chunithm/data/data_chunirec_index.json").read())
def get_difficulty(id):
    if id == "0":
        return "Basic"
    elif id == "1":
        return "Advanced"
    elif id == "2":
        return "Expert"
    elif id == "3":
        return "Master"
    elif id == "4":
        return "Ultima"
    else:
        raise Exception("Invalid difficulty id")

diff_to_chunirec = {
    "0": "BAS",
    "1": "ADV",
    "2": "EXP",
    "3": "MAS",
    "4": "ULT"
}

# def battle(code, cookies):
    
#     return player_name, record, round(best30_total / 30, 4)

def register_favorite(session, code):
    url = "https://chunithm-net-eng.com/mobile/friend/favoriteOn/"
    session.post(
        url, data={"idx": code, "token": session.cookies["_t"]}
    )


def get_friend_list(session):
    url = "https://chunithm-net-eng.com/mobile/friend/"
    response = session.get(url)
    tree = html.fromstring(response.content)
    friend_list = tree.xpath(
        '//div[@class="friend_block"]//div[@class="player_name"]//input[@name="idx"]/@value'
    )
    return friend_list


def invite_friend(session, code):
    url = "https://chunithm-net-eng.com/mobile/friend/search/sendInvite/"
    response = session.post(
        url, data={"idx": code, "token": session.cookies["_t"]}
    )
    tree = html.fromstring(response.content)
    error_msg = tree.xpath('//div[@class="block text_l"]/p[2]/text()')
    if error_msg and error_msg[0] == "Invalid access.":
        raise Exception("Invalid Friend Code")
