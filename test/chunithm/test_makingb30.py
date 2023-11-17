from PIL import Image, ImageDraw, ImageFont

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

    base = Image.open("./blue.PNG").resize((1800, 2000))

    ico = Image.open("./ico.png").convert("RGBA")

    final_ico = Image.new("RGBA", ico.size, color=(255, 255, 255))

    final_ico = Image.alpha_composite(final_ico, ico)

    final_ico = final_ico.resize((180, 180))

    base.paste(final_ico, (60, 40))


    draw = ImageDraw.Draw(base)

    font = ImageFont.truetype("./BAHNSCHRIFT.ttf", 80)
    font_2 = ImageFont.truetype("./BAHNSCHRIFT.ttf", 40)
    font_3 = ImageFont.truetype("./BAHNSCHRIFT.ttf", 64)
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

    count = 0

    for song in data["best"]:
        pic = b30single(song)
        base.paste(pic, (20 + count % 3 * 430, 310 + count // 3 * 168))
        count += 1
    
    count = 0

    for song in data["recent"]:
        pic = b30single(song)
        base.paste(pic, (1350, 310 + count * 168))
        count += 1

    base.save("res.png")
    base.show()

def b30single(data):
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
    
    jacket = Image.open(f'./image/{id}.jpg')
    jacket = jacket.resize((186, 186))
    base.paste(jacket, (32, 28))

    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype('./NotoSansHans-Regular-2.ttf', 37)
    size = font.getlength(title)
    if size > 345:
        title = title[:int(len(title)*(345/size))]
    draw.text((270, 38), title, '#000000', font)

    font_2 = ImageFont.truetype('./BAHNSCHRIFT.TTF', 58)
    draw.text((240, 107), str(score), '#000000', font_2)

    font_3 = ImageFont.truetype('./BAHNSCHRIFT.TTF', 42)
    draw.rectangle((240, 27, 255, 87), fill=color[diff])
    draw.text((240, 177), "Rating: " + str(const) + '  >  ' + str(rating), (0, 0, 0), font_3)

    # 280 105

    base = base.resize((420, 158))
    

    return base

import json

data = json.loads(open("./best30.reiwa5.json").read())

b30make(data)

