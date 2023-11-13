import requests
import time
from aiocqhttp.message import MessageSegment
import difflib
import Levenshtein as lev

token = "0c332b89f58298883d4a60d0c8704f5fa4126a0ec88c9bad76afa411eec4b8c2b9508641e9cdea73964b12bcb8b742fe46d1a72f0074354aa4708d4bcb7679c7"

import json

chuni_data = json.loads(open("./module/chunithm/data/data_chunirec.json").read())
chuni_index = json.loads(open("./module/chunithm/data/data_chunirec_index.json").read())
chuni_unibot = json.loads(open("./module/chunithm/data/data_unibot.json").read())
chuni_alias = json.loads(open("./module/chunithm/data/chuni_alias.json").read())

song = []

keys = chuni_data.keys()

for key in keys:
    song.append(chuni_data[key]["meta"]["title"])


def change_diff(float_num):
    if float_num % 1 == 0.5:
        return str(int(float_num)) + "+"
    else:
        return str(int(float_num))

def csearch(search):

    url = f"https://api.chunirec.net/2.0/music/search.json?q={search}&region=jp2&token={token}"

    request = requests.get(url)

    return request.json()

def calc_similar(s1, s2):
    distance = lev.distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1 - (distance / max_len)

def csearch_all(search):
    csearch_data = csearch(search)

    keys = chuni_alias.keys()

    # 方案A: 使用别名搜索
    for key in keys:
        if search in chuni_alias[key]:
            request = chuni_data[key]
            msg = f"{key}. {request['meta']['title']}\n种类: {request['meta']['genre']}\n艺术家: {request['meta']['artist']}\nBPM: {request['meta']['bpm']}\n更新日期: {request['meta']['release']}\n"
            msg2 = "难度: "
            msg3 = "定数: "
            msg4 = "物量: "

            for diff in ["BAS", "ADV", "EXP", "MAS", "ULT"]:
                if request["data"].get(diff) == None:
                    continue
                msg2 += change_diff(request["data"][diff]["level"]) + "/"
                msg3 += str(request["data"][diff]["const"]) + "/"
                msg4 += str(request["data"][diff]["maxcombo"]) + "/"
            
            msg = msg + msg2[:-1] + "\n" + msg3[:-1] + "\n" + msg4[:-1]

            return msg + MessageSegment.image("https://new.chunithm-net.com/chuni-mobile/html/mobile/img/" + chuni_unibot[key]["jaketFile"])


    if len(csearch_data) == 1: # 方案B: 使用chunirec搜索
        id = csearch_data[0]["id"]

        url = f"https://api.chunirec.net/2.0/music/show.json?id={id}&region=jp2&token={token}"

        request = requests.get(url).json()

        msg = f"{chuni_index[request['meta']['id']]}. {request['meta']['title']}\n种类: {request['meta']['genre']}\n艺术家: {request['meta']['artist']}\nBPM: {request['meta']['bpm']}\n更新日期: {request['meta']['release']}\n"

        msg2 = "难度: "
        msg3 = "定数: "
        msg4 = "物量: "

        for diff in ["BAS", "ADV", "EXP", "MAS", "ULT"]:
            if request["data"].get(diff) == None:
                continue
            msg2 += change_diff(request["data"][diff]["level"]) + "/"
            msg3 += str(request["data"][diff]["const"]) + "/"
            msg4 += str(request["data"][diff]["maxcombo"]) + "/"
        
        msg = msg + msg2[:-1] + "\n" + msg3[:-1] + "\n" + msg4[:-1]

        return msg + MessageSegment.image("https://new.chunithm-net.com/chuni-mobile/html/mobile/img/" + chuni_unibot[chuni_index[request['meta']['id']]]["jaketFile"])
    elif len(csearch_data) > 1:
        msg = ""
        for data in csearch_data:
            msg += chuni_index[data["id"]] + ". " + data["title"] + "\n"
        return msg[:-1]

    # 方案C: 使用模糊搜索

    close_matches = []
    max = 0

    for music in song:
        # close_matches = [] # 永远铭记sb时刻
        similar = calc_similar(search.lower(), music.lower())
        if similar >= max:
            max = similar
        close_matches.append((music, similar))

    
    close_matches = sorted(close_matches, key=lambda x: (x[1]), reverse=True)[:5]

    cutoff = 0.13
    temp = []

    for matches, similar in close_matches:
        if similar >= cutoff:
            temp.append((matches, similar))
    
    close_matches = temp


    # close_matches -> song name
    if len(close_matches) > 1:
        msg = ""
        for matches, similar in close_matches:
            data_search = csearch(matches)
            msg += chuni_index[data_search[0]["id"]] + ". " + data_search[0]["title"] + f" 相似度: {round(similar, 3)}" +"\n"
        return msg[:-1]
    elif len(close_matches) == 1:
        data_search = csearch(close_matches[0][0])
        id = chuni_index[data_search[0]["id"]]
        
        request = chuni_data[id]

        msg = f"{id}. {request['meta']['title']}\n种类: {request['meta']['genre']}\n艺术家: {request['meta']['artist']}\nBPM: {request['meta']['bpm']}\n更新日期: {request['meta']['release']}\n相似度: {round(close_matches[0][1], 3)}\n"
        msg2 = "难度: "
        msg3 = "定数: "
        msg4 = "物量: "

        for diff in ["BAS", "ADV", "EXP", "MAS", "ULT"]:
            if request["data"].get(diff) == None:
                continue
            msg2 += change_diff(request["data"][diff]["level"]) + "/"
            msg3 += str(request["data"][diff]["const"]) + "/"
            msg4 += str(request["data"][diff]["maxcombo"]) + "/"
        
        msg = msg + msg2[:-1] + "\n" + msg3[:-1] + "\n" + msg4[:-1]

        return msg + MessageSegment.image("https://new.chunithm-net.com/chuni-mobile/html/mobile/img/" + chuni_unibot[chuni_index[request['meta']['id']]]["jaketFile"])
    else:
        return "好像没有找到符合的结果"
        

def search_by_id(id):
    request = chuni_data[id]
    msg = f"{chuni_index[request['meta']['id']]}. {request['meta']['title']}\n种类: {request['meta']['genre']}\n艺术家: {request['meta']['artist']}\nBPM: {request['meta']['bpm']}\n更新日期: {request['meta']['release']}\n"

    msg2 = "难度: "
    msg3 = "定数: "
    msg4 = "物量: "

    for diff in ["BAS", "ADV", "EXP", "MAS", "ULT"]:
        if request["data"].get(diff) == None:
            continue
        msg2 += change_diff(request["data"][diff]["level"]) + "/"
        msg3 += str(request["data"][diff]["const"]) + "/"
        msg4 += str(request["data"][diff]["maxcombo"]) + "/"
    
    msg = msg + msg2[:-1] + "\n" + msg3[:-1] + "\n" + msg4[:-1]

    return msg + MessageSegment.image("https://new.chunithm-net.com/chuni-mobile/html/mobile/img/" + chuni_unibot[chuni_index[request['meta']['id']]]["jaketFile"])


import re

def calc(arg1, arg2):
    regex = re.search(r"(c\d+)", arg1)
    if regex == None:
        return "格式不正确 正确格式为: /chuni 分数线 [难度][id] [目标分数]"
    id = regex.group(0)
    diff = None
    for exp in ["绿", "黄", "红", "紫", "黑"]:
        if re.search(exp, arg1) == None:
            continue
        diff = exp
    if diff == None:
        return "格式不正确 正确格式为: /chuni 分数线 [难度][id] [目标分数]"
    index = ["绿", "黄", "红", "紫", "黑"].index(diff)
    diff = ["BAS", "ADV", "EXP", "MAS", "ULT"][index]
    target = int(arg2)

    request = chuni_data[id]
    maxcombo = request["data"][diff]["maxcombo"]
    if maxcombo == 0:
        return "数据库里好像没有这张谱面的物量, 请使用/chuni calc [物量] [目标分数]进行计算"
    
    error = 1010000 - target

    justice_deduct = round(10000 / maxcombo, 2)
    attack_deduct = round(1010000 / (maxcombo * 2), 2)
    miss_deduct = round(1010000 / maxcombo, 2)

    justice_error = round(error / justice_deduct, 2)
    attack_error = round(error / attack_deduct, 2)
    miss_error = round(error / miss_deduct, 2)

    msg = f"[{diff}]{id}. {request['meta']['title']}\n目标分数:{target}\n允许最多JUSTICE数量: {justice_error}(每个-{justice_deduct})\n允许最多ATTACK数量: {attack_error}(每个-{attack_deduct})\n允许最多MISS数量: {miss_error}(每个-{miss_deduct})"
    return msg

def alias(id):
    try:
        alias_try = chuni_alias[id]
        return_msg = ""
        for i in alias_try:
            return_msg += i + ", "
        return return_msg[:-2]
    except:
        return "没有搜寻到相应的别名，请通过/chuni add [曲目id] [别名]进行添加"

def add_alias(id, name):
    try:
        chuni_alias[id].append(name)
    except:
        chuni_alias[id] = [name]
    json_str = json.dumps(chuni_alias)
    open("./module/chunithm/data/chuni_alias.json", "w").write(json_str)