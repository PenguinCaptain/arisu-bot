import random
import time

def sign(user, uid, sender):
    combo = True
    if (time.time() + 8 * 3600) // 86400 > (user[str(uid)]["last_sign"] + 8 * 3600) // 86400 + 1:
        user[str(uid)]["day"] = 0
        combo = False
    elif (time.time() + 8 * 3600) // 86400 <= (user[str(uid)]["last_sign"] + 8 * 3600) // 86400:
        return "你已经签到过了哦"
    user[str(uid)]["day"] = user[str(uid)]["day"] + 1
    user[str(uid)]["last_sign"] = time.time()
    gt_add = int(user[str(uid)]["day"] * 5 + random.randint(100, 200) + user[str(uid)]["hidden_value"] * random.uniform(0.6, 0.9 + user[str(uid)]["lv"] * 0.06)) * 2
    user[str(uid)]["gt"] = user[str(uid)]["gt"] + gt_add
    exp_add = int(gt_add * random.uniform(1, 3) + user[str(uid)]["hidden_value"] * random.uniform(0.34, 0.56 + user[str(uid)]["lv"] * 0.08))
    user[str(uid)]["hidden_value"] = 0
    user[str(uid)]["exp"] = user[str(uid)]["exp"] + exp_add
    while user[str(uid)]["exp"] >= user[str(uid)]["lv"] ** 2 * 100:
        user[str(uid)]["exp"] = user[str(uid)]["exp"] - user[str(uid)]["lv"] ** 2 * 100
        user[str(uid)]["lv"] = user[str(uid)]["lv"] + 1
        user[str(uid)]["gt"] = user[str(uid)]["gt"] + user[str(uid)]["lv"] ** 2 * 8
        gt_add += user[str(uid)]["lv"] ** 2 * 8
    nickname = sender["nickname"]
    message = f"{nickname} Lv.{user[str(uid)]['lv']}\nEXP: {user[str(uid)]['exp']}/{user[str(uid)]['lv'] ** 2 * 100} (+{exp_add})\nGP: {user[str(uid)]['gt']}(+{gt_add})\n你已经连续签到了{user[str(uid)]['day']}天哦~"
    return message

def info(user, uid, sender):
    return f"{sender['nickname']} Lv.{user[str(uid)]['lv']}\nEXP: {user[str(uid)]['exp']}/{user[str(uid)]['lv'] ** 2 * 100}\nGP: {user[str(uid)]['gt']}\n你已经连续签到了{user[str(uid)]['day']}天哦~"