import json


def get_json(filename):
    f = open(filename)
    return json.load(f)


item_list = get_json("mat_list.json")

new_list = {}

for itemtype in item_list.keys():
    for item in item_list[itemtype].keys():

        item_name = item_list[itemtype][item]["name"]

        if (new_list.get(item_name) and "@" in item):
            print (item_name)
            print (new_list.get(item_name))
            item_enchant = item.split("@")[1]
            item_name = item_list[itemtype][item]["name"]+ " ."+item_enchant
            new_list[item_name] = item
        else:
            item_name = item_list[itemtype][item]["name"]
            new_list[item_name] = item


json_obj = json.dumps(new_list, indent=4)

with open("items.json", "w") as outfile:
    outfile.write(json_obj)
