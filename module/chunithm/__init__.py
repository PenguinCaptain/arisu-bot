import module.chunithm.search as search
import module.chunithm.b30 as b30
import json


def handle_command(message, uid):
    try:
        msg = message.split(" ", 2)[1]
        try:
            params = message.split(" ", 2)[2]
        except:
            params = None
        if msg in ["search"]:
            message_return = search.csearch_all(params)
        elif msg in ["id"]:
            message_return = search.search_by_id(params)
        elif msg in ["分数线", "score", "calc"]:
            params = params.split(" ", 2)
            message_return = search.calc(params[0], params[1])
        elif msg in ["alias"]:
            message_return = search.alias(params)
        elif msg in ["add"]:
            params = params.split(" ", 2)
            message_return = search.add_alias(params[0], params[1])
        elif msg in ["b30"]:
            sega_id = json.load(open("./module/chunithm/data/sega_id.json"))
            try:
                data = sega_id[str(uid)]
                message_return = b30.generate_b30(data["account"], data["password"])
            except:
                message_return = "找不到账号密码\n请使用/chuni bind [sega账号] [密码]进行绑定\n注: 只支持国际服的b30查询"
        elif msg in ["bind", "绑定"]:
            params = params.split(" ", 2)
            sega_id = json.load(open("./module/chunithm/data/sega_id.json"))
            sega_id[str(uid)] = {
                "account": params[0],
                "password": params[1]
            }
            open("./module/chunithm/data/sega_id.json", "w").write(json.dumps(sega_id))
            return "绑定成功！请记得撤回你的segaid账号哦"
        else:
            message_return = "暂不支持相关指令 / 没有相关的指令"
    except Exception as e:
        print(e)
        message_return = "会不会是指令打错了?"
    return message_return