import requests
import json
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from aiocqhttp import MessageSegment
import base64
import re

is_ult = False
id = "07059"

def generate_fumen(is_ult, id, diff, title):
    # https://sdvx.in/chunithm/07/bg/07059bg.png
    # https://sdvx.in/chunithm/07/obj/data07059mst.png
    # https://sdvx.in/chunithm/08/jacket/08148.png
    # https://sdvx.in/chunithm/ult/bg/08148bar.png

    if is_ult == True:
        base_url = "https://sdvx.in/chunithm/ult/"
    else:
        base_url = f"https://sdvx.in/chunithm/{id[:2]}/"

    request_bg = requests.get(base_url + f"bg/{id}bg.png")
    request_obj = requests.get(base_url + f"obj/data{id}{diff}.png")
    request_bar = requests.get(base_url + f"bg/{id}bar.png")
    request_img = requests.get(base_url + f"jacket/{id}.png")

    open("src/temp/bg.png", "wb").write(request_bg.content)
    open("src/temp/obj.png", "wb").write(request_obj.content)
    open("src/temp/bar.png", "wb").write(request_bar.content)
    open("src/temp/img.png", "wb").write(request_img.content)

    bg = Image.open("src/temp/bg.png").convert("RGBA")
    obj = Image.open("src/temp/obj.png").convert("RGBA")
    bar = Image.open("src/temp/bar.png").convert("RGBA")
    img = Image.open("src/temp/img.png").resize((110, 110))

    font = ImageFont.truetype('./src/chunithm/font/NotoSansHans-Regular-2.ttf', 60)
    font_2 = ImageFont.truetype('./src/chunithm/font/BAHNSCHRIFT.TTF', 45)

    size = bg.size
    size = (size[0], size[1] + 145)

    background = Image.new("RGBA", size, (0, 0, 0))

    background.paste(bg, mask=bg)
    background.paste(obj, mask=obj)
    background.paste(bar, mask=bar)
    

    draw = ImageDraw.Draw(background)
    background.paste(img, (25, size[1] - 130))
    draw.text((160, size[1] - 130), f"{title} [{diff.upper()}]", "#ffffff", font)
    draw.text((160, size[1] - 55), "Generated from website https://sdvx.in", "#ffffff", font_2)

    # background = background.resize((3200, int(3200 / background.size[0] * background.size[1])))

    background.save("src/fumen.png")
    
    return "[CQ:image,file=file:////Users/a1231/Downloads/qqbot_v2/src/fumen.png]"

diff_change = {"红": "exp", "紫": "mst", "黑": "ult"}
chunirec = json.loads(open("./module/chunithm/data/data_chunirec.json").read())
sdvxin = json.loads(open("./module/chunithm/data/sdvx.in.json").read())

def handle_fumen(id):
    is_ult = False
    try:
        temp = id.split("c")
    except:
        return "你没有输入正确的指令哦\n正确指令是: \chuni chart [难度][id]\n而且只能查询红, 紫, 黑三个难度"
    if temp[0] == "黑": 
        is_ult = True
    title = chunirec["c" + temp[1]]["meta"]["title"]
    diff = diff_change[temp[0]]
    sdvx_id = sdvxin[title]
    return generate_fumen(is_ult, sdvx_id, diff, title)

handle_fumen("紫c257")
