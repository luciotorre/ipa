import csv
import sys
import os
import json

path = sys.argv[1]

def flatten_dict(key, value):
    if isinstance(value, list):
        return
    if isinstance(value, tuple):
        return
    if isinstance(value, dict):
        for k, v in value.items():
            for nk, nv in flatten_dict(k, v):
                yield key + "_" + nk, nv
    else:
        yield key, value

items = []
keys = set()
for f in os.listdir(path):
    data = json.load(open(path + "/" + f))
    item = {}
    for k in data:
        for nk, nv in flatten_dict(k, data[k]):
            item[nk] = nv
            keys.add(nk)
    items.append(item)

print(sorted(keys))
with open('start.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=sorted(keys))

    writer.writeheader()
    for item in items:
        writer.writerow(item)
