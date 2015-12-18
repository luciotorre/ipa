import sys
import os
import json

path = sys.argv[1]


prices = []
for f in os.listdir(path):
    data = json.load(open(path + "/" + f))
    if data["currency_id"] != "ARS":
        continue

    try:
        p = float(data['price'])
    except:
        pass
    prices.append(p)

prices.sort()
tot = len(prices)

print("total items:", tot)
print("average:", sum(prices) / tot)
print("max:", max(prices))
print("min:", min(prices))
print("50p:", prices[int(tot * 0.5)])
print("25p:", prices[int(tot * 0.25)])
print("75p:", prices[int(tot * 0.75)])
print("10p:", prices[int(tot * 0.1)])
print("90p:", prices[int(tot * 0.9)])
print("sum:", "{0:.4e}".format(sum(prices)))
edge = int(tot * 0.01)
#snipped = prices[edge:-edge]
snipped = prices[edge:-edge]
print("snipped avg", sum(snipped) / len(snipped) )
ipa = sum(snipped) / len(snipped) * 8900 / 6807.121149322091
print ("ipa", ipa)
