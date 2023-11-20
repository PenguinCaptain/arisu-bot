import module.chunithm.search as search
import module.chunithm.b30 as b30
import module.chunithm.fumen as fumen
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
                if params == None:
                    data_en = sega_id[str(uid)]["en"]
                elif params == "jp":
                    data_jp = sega_id[str(uid)]["jp"]
                elif params == "cn":
                    pass
            except:
                message_return = "找不到账号密码\n国际服:请使用/chuni bind [sega账号] [密码] or /chuni bind [好友码] fc 进行绑定\n日服:请使用/chuni bind [chunirec ユーザーID] jp 进行绑定\n国服: 请使用/chuni b30 cn进行查询 不需要绑定"
                return message_return
            if params == None:
                message_return = b30.generate_b30(data_en["account"], data_en["password"])
            elif params == "jp":
                message_return = b30.generate_b30_jp(data_jp["name"])
            elif params == "cn":
                message_return = b30.generate_b30_cn(uid)
            return message_return
            
        elif msg in ["bind", "绑定"]:
            params = params.split(" ", 2)
            sega_id = json.load(open("./module/chunithm/data/sega_id.json"))
            if sega_id.get(str(uid)) == None:
                sega_id[str(uid)] = {
                    "en": {},
                    "en_frd": {},
                    "jp": {}
                }
            if params[1] == "jp":
                sega_id[str(uid)]["jp"] = {
                    "name": params[0]
                }
            else:
                sega_id[str(uid)]["en"] = {
                    "account": params[0],
                    "password": params[1]
                }
            open("./module/chunithm/data/sega_id.json", "w").write(json.dumps(sega_id))
            return "绑定成功！请记得撤回你的segaid账号哦"
        elif msg in ["谱面预览", "谱", "谱面", "chart", "fumen", "fm"]:
            message_return = fumen.handle_fumen(params)
        else:
            message_return = "暂不支持相关指令 / 没有相关的指令"
    except Exception as e:
        print(e)
        message_return = "会不会是指令打错了?"
    return message_return