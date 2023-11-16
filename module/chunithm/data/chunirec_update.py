import requests
import re

token = "0c332b89f58298883d4a60d0c8704f5fa4126a0ec88c9bad76afa411eec4b8c2b9508641e9cdea73964b12bcb8b742fe46d1a72f0074354aa4708d4bcb7679c7"

def data_showall():
    url = f"https://api.chunirec.net/2.0/music/showall.json?region=jp2&token={token}"
    request = requests.get(url)
    return request.json()

import json

chunithm_data = json.loads(open("./module/chunithm/data/data_unibot.json").read())

key = chunithm_data.keys()

data1 = {}
data2 = {}
data3 = {}
data4 = {}

for data in data_showall():
    # for chuni_data in chunithm_data:
    for single_key in key:
        chuni_data = chunithm_data[single_key]
        if (chuni_data["title"] == data["meta"]["title"] and int(chuni_data["id"]) < 8000) or (data["meta"]["title"].startswith(chuni_data["title"]) and int(chuni_data["id"]) >= 8000 and re.search("】", data["meta"]["title"]) != None):
            data1["c" + str(chuni_data["id"])] = data
            data2[data["meta"]["id"]] = "c" + str(chuni_data["id"])
            data4[data["meta"]["title"]] = data
            continue

# for chuni_data in chunithm_data:
for single_key in key:
    chuni_data = chunithm_data[single_key]
    data3["c" + chuni_data["id"]] = chuni_data

open("./module/chunithm/data/data_chunirec.json", "w").write(json.dumps(data1))
open("./module/chunithm/data/data_chunirec_index.json", "w").write(json.dumps(data2))
open("./module/chunithm/data/data_unibot.json", "w").write(json.dumps(data3))
open("./module/chunithm/data/data_song_to_const.json", "w").write(json.dumps(data4))



# for chuni_data in data_showall():
#     if chuni_data["meta"]["genre"] == "WORLD'S END":
#         num = code_we
#         code_we += 1
#     else:
#         num = code
#         code += 1
#     chuni_code[chuni_data["meta"]["id"]] = "c" + str(num)
    
# open("data_index.json", "w").write(json.dumps(chuni_code))