level = 0
m = 0
c = 114514
while c >= m:
    m += 10 * 2 ** (level // 10)
    level += 1

print(level)