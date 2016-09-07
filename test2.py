def counter(word):
    d = {}
    for c in word:
        d[c] = d.get(c, 0) + 1
    return d

print counter('johnjjjjj')