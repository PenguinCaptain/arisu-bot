def score_to_rating(score, const):
    import math
    # rating transformer
    if score > 1009000:
        rating = const + 2.15
    elif score > 1007500:
        rating = const + 2 + (score - 1007500) / (1009000 - 1007500) * 0.15
    elif score > 1005000:
        rating = const + 1.5 + (score - 1005000) / (1007500 - 1005000) * 0.5
    elif score > 1000000:
        rating = const + 1 + (score - 1000000) / (1005000 - 1000000) * 0.5
    elif score > 975000:
        rating = const + 0 + (score - 975000) / (1000000 - 975000) * 1
    elif score > 925000:
        rating = const + -3 + (score - 925000) / (975000 - 925000) * 3
    elif score > 900000:
        rating = const + -5 + (score - 900000) / (925000 - 900000) * 2
    elif score > 800000:
        rating = (const - 5) / 2 + (score - 800000) / (900000 - 800000) * ((const + -5) - (const - 5) / 2)
    elif score > 500000:
        rating = 0 + (score - 500000) / (800000 - 500000) * (const - 5) / 2
    else:
        rating = 0
    return math.floor(rating*100)/100

import json
data = json.loads(open("./data_song_to_const.json").read())

def song_to_rating(name, diff, score):
    
    const = data[name]["data"][diff]["const"]
    rating = score_to_rating(score, const)
    return rating, const