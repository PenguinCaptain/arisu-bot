import pyppeteer
import asyncio
import requests
import json
from http.cookiejar import CookiePolicy
from lxml import html
from calc_score import *

CHUNITHM_INTL_SEGA_ID = "acekuro0219"
CHUNITHM_INTL_SEGA_PASSWORD = "gzycTaffyxxm0915"
CHUNITHM_TARGET_FRIEND_CODE = "9063147588258"


if not CHUNITHM_INTL_SEGA_ID or not CHUNITHM_INTL_SEGA_PASSWORD:
    raise Exception("Please set CHUNITHM_INTL_SEGA_ID and CHUNITHM_INTL_SEGA_PASSWORD")

if not CHUNITHM_TARGET_FRIEND_CODE:
    raise Exception("Please set CHUNITHM_TARGET_FRIEND_CODE")


class CustomCookiePolicy(CookiePolicy):
    def set_ok(self, cookie, _):
        if cookie.name == "friendCodeList":
            return True
        return False

    return_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False

    netscape = True
    rfc2965 = hide_cookie2 = False


async def main():
    cookies = await get_cookies()
    session = requests.Session()
    session.cookies.update({"userId": cookies["userId"], "_t": cookies["_t"]})
    session.cookies.set_policy(CustomCookiePolicy())

    print("Fetching friend list...")
    friend_list = get_friend_list(session)

    if CHUNITHM_TARGET_FRIEND_CODE not in friend_list:
        invite_friend(session)
        print("Not a friend, invite sent")
        return

    print("Registering as favorite...")
    register_favorite(session)

    print("Fetching record...")
    player_name, record = battle(session)

    data = {
        "player_name": player_name,
        "best": record
    }

    print("Saving record...")
    with open("best30.fetchByFrdCode.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data


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


def battle(session):
    url = "https://chunithm-net-eng.com/mobile/friend/genreVs/sendBattleStart/"
    record = []

    for i in range(4):
        response = session.post(
            url,
            data={
                "genre": "99",
                "friend": CHUNITHM_TARGET_FRIEND_CODE,
                "radio_diff": str(i),
                "token": session.cookies["_t"],
            },
        )

        tree = html.fromstring(response.content)

        player_name = tree.xpath('//*[@id="inner"]/div[3]/div[2]/div[3]/form/div[1]/select[2]/option/text()')[0]

        music_boxes = tree.xpath('//div[contains(@class, "music_box")]')

        print(player_name, type(player_name))

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
            
            rating = song_to_rating(music_name, diff_to_chunirec[str(i)], score)

            record.append(
                {
                    "music_name": music_name,
                    "difficulty": get_difficulty(str(i)),
                    "score": score,
                    "rating": rating,
                    "is_fc": isFC,
                    "is_aj": isAJ,
                }
            )
        record = sorted(record, key=lambda x: (x["rating"]), reverse=True)
    return player_name, record


def register_favorite(session):
    url = "https://chunithm-net-eng.com/mobile/friend/favoriteOn/"
    session.post(
        url, data={"idx": CHUNITHM_TARGET_FRIEND_CODE, "token": session.cookies["_t"]}
    )


def get_friend_list(session):
    url = "https://chunithm-net-eng.com/mobile/friend/"
    response = session.get(url)
    tree = html.fromstring(response.content)
    friend_list = tree.xpath(
        '//div[@class="friend_block"]//div[@class="player_name"]//input[@name="idx"]/@value'
    )
    return friend_list


def invite_friend(session):
    url = "https://chunithm-net-eng.com/mobile/friend/search/sendInvite/"
    response = session.post(
        url, data={"idx": CHUNITHM_TARGET_FRIEND_CODE, "token": session.cookies["_t"]}
    )
    tree = html.fromstring(response.content)
    error_msg = tree.xpath('//div[@class="block text_l"]/p[2]/text()')
    if error_msg and error_msg[0] == "Invalid access.":
        raise Exception("Invalid Friend Code")


async def get_cookies():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    login_url = "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=chuniex&redirect_url=https://chunithm-net-eng.com/mobile/"
    print("Opening login page...")
    await page.goto(login_url)
    await page.click(".c-button--openid--segaId")
    await page.type("#sid", CHUNITHM_INTL_SEGA_ID)
    await page.type("#password", CHUNITHM_INTL_SEGA_PASSWORD)

    print("Logging in...")
    await asyncio.gather(page.waitForNavigation(), page.click("#btnSubmit"))

    cookies = await page.cookies()
    await browser.close()
    # make cookies dict only with name and value
    cookies = {cookie["name"]: cookie["value"] for cookie in cookies}
    return cookies


if __name__ == "__main__":
    data = asyncio.get_event_loop().run_until_complete(main())
    print(data)
