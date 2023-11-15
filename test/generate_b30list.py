from bs4 import BeautifulSoup
import json

content = open("./best30_4445256934383693.html").read()

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

#inner > div.frame01.w460 > div.frame01_inside.w460 > div.w420.box01 > div.box05.w400 > form:nth-child(1)