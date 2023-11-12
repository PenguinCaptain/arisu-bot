import module.user.dogbark as dogbark
import module.user.sign as sign

def handle_command(uid, gid, message, user, sender, nickname):
    try:
        msg = message.split(" ", 2)[1]
        if msg in ["狗叫", "我的狗叫", "dogbark", "db"]:
            message_return = dogbark.get_dogbark_info(uid, user, sender["nickname"], message, nickname)
        elif msg in ["stat"]:
            message_return = dogbark.get_stat(user)
        elif msg in ["狗叫排行", "rank"]:
            message_return = dogbark.get_dogbark_rank(user, uid, sender, nickname)
        elif msg in ["今日狗叫排行", "dlrank"]:
            message_return = dogbark.get_daily_dogbark_rank(user, uid, sender, nickname)
        elif msg in ["签到", "s", "sign"]:
            message_return = sign.sign(user, uid, sender)
        elif msg in ["个人信息", "info"]:
            message_return = sign.info(user, uid, sender)
        elif msg in ["添加关键词", "word"]:
            message_return = dogbark.append_wordings(message)
        else:
            message_return = "暂不支持相关指令 / 没有相关的指令"
    except Exception as e:
        print(e)
        message_return = "会不会是指令打错了?"
    # print(message_return)
    return message_return
    