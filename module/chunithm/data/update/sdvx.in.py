import requests
from bs4 import BeautifulSoup
import json


sdvx_in_data = {}

base = "https://sdvx.in/chunithm/sort/"

for diff in ["11", "11+", "12", "12+", "13", "13+", "14", "14+", "15"]:
    request = requests.get(f"{base}{diff}.htm")
    request.encoding = 'utf-8'
    soup = BeautifulSoup(request.text, 'html.parser')
    scripts = soup.find_all("script")

    for script in scripts:
        if script.string:
            content = script.string
            if content.startswith("SORT") and content != "SORTLEVEL00();":
                try:
                    song_id = content.split('()')[0].replace('SORT', '')
                    if song_id[-1] != "M":
                        continue
                    else:
                        song_id = song_id[:-1]
                    title = script.find_next_sibling(string=True)
                    sdvx_in_data[title] = song_id
                except:
                    pass

open("sdvx.in.json", "w").write(json.dumps(sdvx_in_data, ensure_ascii=False))