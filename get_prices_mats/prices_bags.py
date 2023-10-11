import sys
sys.path.append('../Albion Scraper')

import albion_prices_helper as prices

def main():
    item_list = prices.get_json("item_json_separated.json")
    item_type_keyword = "_BAG"
    item_type = "Bags"
    location = "Thetford"
    qualities = "1,2,3"
    prices.get_and_save_item_types(
        item_type, item_type_keyword, location, qualities, item_list)


main()
