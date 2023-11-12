import module.malody.calc as calc

def handle_command(message):
    msg = message.split(" ", 3)
    cmd = msg[1]
    try:
        if cmd == "calc":
            return calc.return_msg(msg[2], msg[3])
        else:
            return "暂不支持相关指令"
    except:
        return "会不会是指令打错了?"