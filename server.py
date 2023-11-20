from aiocqhttp import CQHttp, Event
import json
import time
import module.user, module.chunithm, module.malody
import random
from html import unescape
from urllib.parse import quote
import re

bot = CQHttp()

# 预加载项

user = json.loads(open("./data/user.json").read())
init = json.loads(open("./data/init.json").read())
nickname = json.loads(open("./data/nickname.json").read())
dogbark = open("./src/dogbark.txt").read().splitlines()

user_init = { "gt": 0,
        "lv": 1,
        "exp": 0,
        "last_sign": 0,
        "day": 1,
        "jrys": {},
        "hidden_value": 0,
        "dogbark": {
            "dogbark_count": 0,
            "today_dogbark": 0,
            "last_dogbark": 0
        },
        "daphnis": {
            "length": 0,
            "last_time": 0,
            "maximum": 0,
            "minimum": 0,
            "count": 10
        }
}

def message_to_cq(message): # 将event.message转义成原先的cq码
    message_merged = ""
    for msg in message:
        if msg["type"] == "text":
            message_merged += msg["data"]["text"]
        else:
            key_list = msg["data"].keys()
            type = msg["type"]
            params = ""
            for key in key_list:
                params += "," + key + "=" + msg["data"][key]
            message_merged += f"[CQ:{type}{params}]"
    return message_merged

# handle commands
@bot.on_message
async def _(event: Event):
    
    gid = event.group_id # 群号 / message.private -> None
    uid = event.user_id # QQ号
    if uid == event.self_id or gid in [624670021]: # 过滤掉自己发送的消息
        return
    message = unescape(event.message)
    message_cq = message_to_cq(message)
    sender = event.sender # message.private -> {} / message.group ->　dataがある
    try:
        nickname[str(uid)] = sender["nickname"] # 保存每一个人的QQ昵称
    except:
        pass
    
    call = False
    if message_cq.startswith("/江江"): # 江江模块 分割到plugin/user/__init__.py进行处理再返回
        message_return = module.user.handle_command(uid, gid, message_cq, user, sender, nickname)
        try:
            await bot.send(event, message_return) # 注: 我求你了不要在发信息的时候漏了写event这个参数！！！！！！
        # 注：请记得加上await！！！！
            if message_return == "updated":
                dogbark = open("./src/dogbark.txt").read().splitlines()
        except:
            pass
    elif message_cq.startswith("/chuni"): # chunithm模块
        message_return = module.chunithm.handle_command(message_cq, uid)
        try:
            if message_return == None:
                return
            await bot.send(event, message_return) # 注: 我求你了不要在发信息的时候漏了写event这个参数！！！！！！
        # 注：请记得加上await！！！！
        except:
            pass
    elif message_cq.startswith("/malody"):
        message_return = module.malody.handle_command(message_cq)
        try:
            await bot.send(event, message_return) # 注: 我求你了不要在发信息的时候漏了写event这个参数！！！！！！
        # 注：请记得加上await！！！！
        except:
            pass
    elif message_cq == "/保存": # 保存数据 用于调试
        json_content_str = json.dumps(user)
        open("./data/user.json", "w").write(json_content_str) # 保存 应该狗叫就够
        json_content_str = json.dumps(nickname)
        open("./data/nickname.json", "w").write(json_content_str)
        print("保存成功")
    else: 
        return

    print(uid, gid, message_cq)

            


@bot.on_message("group") # 单独检测狗叫模块
async def handle_dogbark_message(event: Event):
    uid = event.user_id
    gid = event.group_id
    if uid == event.self_id or gid in [624670021]: # 过滤掉自己发送的消息
        return
    message_cq = message_to_cq(event.message)
    dogbark = open("./src/dogbark.txt").read().splitlines()
    # flag = False
    # for temp in dogbark:
    #     if re.search(temp, message_cq) != None:
    #         print(temp)
    #         flag = True
    # if flag == True:
    if any(re.search(temp, message_cq) != None for temp in dogbark): # 用any函数检查message_cq变量中是否含有dogbark中的其中一个元素 鉴定狗叫 -> bool
        print(message_cq + "->" + "狗叫")
        try:
            user[str(uid)]["dogbark"]["dogbark_count"] += 1
        except:
            user[str(uid)] = user_init
            user[str(uid)]["dogbark"]["dogbark_count"] += 1
        user[str(uid)]["dogbark"]["today_dogbark"] += 1
        user[str(uid)]["dogbark"]["last_dogbark"] = time.time()
        json_content_str = json.dumps(user)
        open("./data/user.json", "w").write(json_content_str) # 保存 应该狗叫就够
        json_content_str = json.dumps(nickname)
        open("./data/nickname.json", "w").write(json_content_str)
    if ( time.time() + (8 * 3600) ) // 86400 > ( init["check_dogbark"] + (8 * 3600) ) // 86400:
        user_uidList = list(user.keys())
        # random.shuffle(user_uidList)
        # dogbark = []
        # for id in user_uidList:
        #     dogbark.append((id, user[id]["dogbark"]["today_dogbark"]))
        #     dogbark = sorted(dogbark, key=lambda x: (x[1]), reverse=True)
        for id in user_uidList:
            user[id]["hidden_value"] = user[id]["hidden_value"] + int(user[id]["dogbark"]["today_dogbark"] * (user[id]["lv"] ** 2) // 10)
            user[id]["dogbark"]["today_dogbark"] = 0
        init["check_dogbark"] = time.time()
        json_content_str = json.dumps(init)
        open("./data/init.json", "w").write(json_content_str)
        json_content_str = json.dumps(user)
        open("./data/user.json", "w").write(json_content_str) # 保存 应该狗叫就够
        # yesterday = time.strftime(r"%Y/%m/%d", time.localtime(time.time() - 86400))
        # try:
        #     nickname_dbking = nickname[str(dogbark[0][0])]
        # except:
        #     nickname_dbking = dogbark[0][0]
        # message = f"{nickname_dbking}({dogbark[0][0]})是昨天({yesterday})的狗叫王, 一共狗叫了{dogbark[0][1]}次, 恭喜捏"
        # print(message)
        # for group in init["white_list"]:
        #     await bot.send_group_msg(self_id=event.self_id, group_id=729529363, message=message)
    
bot.run(host='127.0.0.1', port=8080)