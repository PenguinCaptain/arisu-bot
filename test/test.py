import difflib
import json

search = "requiem"

chuni_data = json.loads(open("./module/chunithm/data/data_chunirec.json").read())
chuni_index = json.loads(open("./module/chunithm/data/data_chunirec_index.json").read())
chuni_unibot = json.loads(open("./module/chunithm/data/data_unibot.json").read())
chuni_alias = json.loads(open("./module/chunithm/data/chuni_alias.json").read())

song = []

keys = chuni_data.keys()

for key in keys:
    song.append(chuni_data[key]["meta"]["title"])


close_matches = difflib.get_close_matches(search, song, n=10, cutoff=0.4)
print(close_matches)