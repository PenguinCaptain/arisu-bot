import json

data_chunirec = json.loads(open("./module/chunithm/data/data_chunirec.json").read())
data_unibot = json.loads(open("./module/chunithm/data/data_unibot.json").read())

data_key = data_chunirec.keys()

up_const = 14.4
low_const = 14.0

const_dict = {}

for const in range(int(low_const * 10), int(up_const * 10) + 1, 1):
    key = str(const / 10)
    if const / 10 == 14.0:
        key = "14"
    const_dict[key] = []

for key in data_key:
    if int(key[1:]) >= 8000:
        continue
    data = data_chunirec[key]["data"]
    image = data_unibot[key]["jaketFile"]
    try:
        const_exp = data["EXP"]["const"]
        const_mas = data["MAS"]["const"]
        const_ult = data["ULT"]["const"]
    except:
        const_ult = 0
    if low_const <= const_exp <= up_const:
        const_dict[str(const_exp)].append((image, "EXP"))

for key in data_key:
    if int(key[1:]) >= 8000:
        continue
    data = data_chunirec[key]["data"]
    image = data_unibot[key]["jaketFile"]
    try:
        const_exp = data["EXP"]["const"]
        const_mas = data["MAS"]["const"]
        const_ult = data["ULT"]["const"]
    except:
        const_ult = 0
    if low_const <= const_mas <= up_const:
        const_dict[str(const_mas)].append((image, "MAS"))

for key in data_key:
    if int(key[1:]) >= 8000:
        continue
    data = data_chunirec[key]["data"]
    image = data_unibot[key]["jaketFile"]
    try:
        const_exp = data["EXP"]["const"]
        const_mas = data["MAS"]["const"]
        const_ult = data["ULT"]["const"]
    except:
        const_ult = 0
    if low_const <= const_ult <= up_const:
        const_dict[str(const_ult)].append((image, "ULT"))


        
