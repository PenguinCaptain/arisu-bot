import module.chunithm.search as search


def handle_command(message):
    try:
        msg = message.split(" ", 2)[1]
        params = message.split(" ", 2)[2]
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
        else:
            message_return = "暂不支持相关指令 / 没有相关的指令"
    except Exception as e:
        print(e)
        message_return = "会不会是指令打错了?"
    print(message_return)
    return message_return