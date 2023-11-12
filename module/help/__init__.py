help = open("./module/help/help.txt").read()

def handle_command(message):
    try:
        command = message.split(" ", 1)[1]
    except:
        command = ""
    if command in [""]:
        return help
    else:
        return "暂不支持相关指令"
    
