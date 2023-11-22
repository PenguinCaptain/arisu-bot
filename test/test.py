import math

decimal = 114.5141919
place = 4

def truncate_decimal(decimal, place):
    return float(f"%.{place}f" % float(math.floor(decimal * 10 ** place) / (10 ** place)))

print(truncate_decimal(decimal, place))