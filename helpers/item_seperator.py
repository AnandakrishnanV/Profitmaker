
import json

def get_json(filename):  
    f = open(filename)  
    return json.load(f)

def separator(item_list):
    new_list = {}
    item_type_array = ["_GATHERER","UNIQUE","_ARTEFACT", "_OFF_","_CAPEITEM_","_CAPE_","_BAG","_2H_","_MOUNT_","_HEAD_","_ARMOR_","_SHOES_","_BACKPACK_","_MAIN_","_RUNE","_SOUL","_RELIC","_SHARD", "_ESSENCE_POTION","_ESSENCE","_ROCK","_WOOD","_FIBER","_HIDE","_ORE"]
    for item in item_list:
        for item_type in item_type_array:

            if item_type in item:
                if not new_list.get(item_type):
                    new_list[item_type] = {}
                    
                new_list[item_type][item] = item_list[item] 
                if len(item.split("_")) > 2:
                    new_list[item_type][item]["TYPE"] = item.split("_")[2].split("@")[0]
                if len(item.split("@")) > 1 :
                    new_list[item_type][item]["ENCHANT_LEVEL"] = item.split("@")[1]

                tier = item.split("_")[0]
                if tier[0] != "T":
                    new_list[item_type][item]["TIER"] = tier
                else:
                    new_list[item_type][item]["TIER"] = int(tier[1])
                break

    return new_list

def set_count(new_list: dict):
    
    for item_type in new_list:
        new_list[item_type]["COUNT"] = len(new_list[item_type].keys())                

item_list = get_json("item_json.json")
new_list = separator(item_list)
set_count(new_list)


json_obj = json.dumps(new_list, indent=4)

with open("item_json_seperated.json", "w") as outfile:
    outfile.write(json_obj)