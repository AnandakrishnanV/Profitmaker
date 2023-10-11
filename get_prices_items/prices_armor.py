import math
import sys
import pandas as pd
sys.path.append('../Albion Scraper')
import albion_prices_helper as prices


def split_to_fit(item_list, item_type_keyword):

    new_item_list = list(item_list[item_type_keyword].keys())
    if "COUNT" in new_item_list:
        new_item_list.remove("COUNT")
    no_of_items = len(new_item_list)
    total_size = len(",".join(new_item_list))

    divisor = int(no_of_items/math.ceil(total_size/3500))
    chunks = [new_item_list[x:x+divisor]
              for x in range(0, no_of_items, divisor)]

    str_chunks = []
    for chunk in chunks:
        str_chunks.append((",".join(chunk)))

    return str_chunks


def get_armor(locations):
    item_list = prices.get_json("item_json_seperated.json")
    item_type_keyword = "_ARMOR_"
    new_item_list = split_to_fit(item_list, item_type_keyword)
    item_type = "Items_Armor"
    location = locations
    qualities = None

    final_df = pd.DataFrame()

    for items in new_item_list:
        new_df = prices.get_item_types(items, location, qualities, True)
        final_df = pd.concat([final_df, new_df], ignore_index=True) 

    prices.save_item_prices(item_type, final_df)

if __name__ == "__main__":
    get_armor("")
