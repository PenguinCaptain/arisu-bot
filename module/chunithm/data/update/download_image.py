import json, requests

chunithm_data = json.loads(open("../module/chunithm/data/data_unibot.json").read())

for key in chunithm_data.keys():
    url = "https://new.chunithm-net.com/chuni-mobile/html/mobile/img/" + chunithm_data[key]["image"]
    request = requests.get(url)
    open(f"./image/{key}.jpg", "wb").write(request.content)
    print(key)