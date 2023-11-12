import random

guess_list = {
    "arcaea": open("src/guess_list/arcaea.txt").read().splitlines(),
    "chunithm": open("src/guess_list/chu.txt").read().splitlines()
}

song_guess_data = {}

# 1. 随机曲目
def generate_question(song_list, num=10):

    answer = []

    # 把曲库调出来
    seed = []
    for s in song_list:
        seed.append(guess_list[s])

    n = 0
    while n < num:
        # 随机曲库
        list = random.randint(0, len(seed) - 1)
        # 随机曲目
        random_value = random.randint(0, len(seed[list]) - 1)

        while seed[list][random_value] in answer:
            random_value = random.randint(0, len(seed[list]) - 1)
        
        answer.append(seed[list][random_value])
        n += 1
    
    # 目前是已经把answer弄出来了，下一步是隐藏answer
    
    display = []

    for ans in answer:
        display_word = ""
        for char in ans:
            if char != " ":
                display_word += "*"
            else:
                display_word += " "
        display.append(display_word)
    return answer, display

# 2. 把随机出来的曲库变成一个字典格式 (后续会重用) 目的是为了方便日后添加更多的功能然后不用到处改

def generate_dict(answer, display, char, player, msg_id, argument):

    # 计算correct的数量

    correct = 0

    print(len(display))

    for n in range(0, len(display)):
        if display[n] == answer[n]:
            correct += 1

    return {
        "display": display,
        "answer": answer,
        "guessed_char": char,
        "player": player,
        "correct": correct,
        "msg_id": msg_id,
        "argument": argument
    }

def guess(type, dict, guess_string, uid):
    try:
        if type == "char":
            if guess_string in dict["guessed_char"]: # 检查如果有重复char则返回错误
                return dict, -1
            score = -5
            for i in range(0, len(dict["answer"])):
                display = list(dict["display"][i])
                answer = dict["answer"][i]
                for j in range(0, len(answer)):
                    if answer[j] == guess_string.lower() or answer[j] == guess_string.upper():
                        display[j] = answer[j]
                        score += 1
                dict["display"][i] = "".join(display)
            dict["guessed_char"] += guess_string
            display = dict["display"]
            answer = dict["answer"]
        
        elif type == "song":
            answer = dict["answer"]
            display = dict["display"]
            score = -10
            for i in range(0, len(answer)):
                if guess_string.lower() == answer[i].lower():
                    score += 20
                    display[i] = answer[i]
                    break
        
        # 给玩家加分

        if dict["player"].get(str(uid)) == None:
            dict["player"][str(uid)] = 0
        dict["player"][str(uid)] += score
        

        dict = generate_dict(
            answer, 
            display, 
            dict["guessed_char"], 
            dict["player"], 
            dict["msg_id"], 
            dict["argument"]
        )
    except:
        return dict, -2
    
    return dict, 0
            
def check_game_end(dict):
    display = dict["display"]
    answer = dict["answer"]
    count = 0
    for i in range(0, len(display)):
        if display[i] == answer[i]:
            count += 1
    if count == len(display):
        flag = True
    else:
        flag = False
    return flag