import requests
import time
import datetime
import os
import json


def get_categories():
    cats = {}
    r = requests.get("https://api.mercadolibre.com/sites/MLA/categories")
    for cat in r.json():
        cats[cat["id"]] = cat["name"]

    return cats


def lister(category):
    url_template = "https://api.mercadolibre.com/sites/MLA/search?limit=%s&offset=%s&category=%s&since=today&condition=new&buying_mode=buy_it_now"
    total = 500
    offset = 0
    limit = 50

    while offset + limit < total:
        url = url_template % (limit, offset, category)
        r = requests.get(url)
        for row in r.json()['results']:
            if "Item De Testeo, Por Favor No Ofertar" in row['title']:
                continue
            yield row

        offset += limit


outdir = datetime.datetime.now().isoformat()

categories = get_categories()
print(categories)
catdir = os.path.join(outdir, "categories")
objdir = os.path.join(outdir, "items")

def save(directory, name, dictionary):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, name), "w") as fh:
        json.dump(dictionary, fh)

for ck in categories:
    r = requests.get("https://api.mercadolibre.com/categories/%s" %(ck,))
    d = r.json()
    print (ck, categories[ck], "Cantidad a la venta:", d["total_items_in_this_category"])
    save(catdir, ck, d)


for category in categories:
    print("%s --------------------------------" % (category,))

    done = False
    while not done:
        try:
            items = []
            for item in lister(category):
                print(item['id'], item['title'], item['price'])
                items.append(item)
            done = True
        except requests.exceptions.ConnectionError as exc:
            print("error, restarting category")
            print(exc)
            time.sleep(20)
            continue

        for o in items:
            save(objdir, o['id'], o)
