import sys
sys.path.append('../Albion Scraper')

import albion_prices_helper as prices


def get_cloth(locations):
    item_list = prices.get_json("item_json_seperated.json")
    item_type_keyword = "_CLOTH"
    item_type = "Refined_Cloth"
    location = locations
    qualities = None
    prices.get_and_save_item_types(
        item_type, item_type_keyword, location, qualities, item_list, True)

