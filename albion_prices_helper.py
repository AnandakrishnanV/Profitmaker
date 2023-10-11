import albion_prices_api as prices_api
import json
import pandas as pd


def remove_elements_with_character(lst, character):
    return [item for item in lst if character not in item]


def get_json(filename):
    f = open(filename)
    return json.load(f)


def set_item_types(item_list, item_type_keyword):
    item_type_list = list(item_list[item_type_keyword].keys())
    if "COUNT" in item_type_list:
        item_type_list.remove("COUNT")
    joined_list = (",".join(item_type_list))
    return joined_list


def get_and_save_item_types(item_type, item_type_keyword, location, qualities, item_list, sort_mats):
    items = set_item_types(item_list, item_type_keyword)
    response = prices_api.call_albion_api(items, location, qualities)
    prices_api.save_to_file("sheets\\"+item_type, response, sort_mats)


def get_item_types(items, location, qualities, sort_mats):
    response = prices_api.call_albion_api(items, location, qualities)
    return prices_api.return_df(response, sort_mats)


def save_item_prices(item_type, data: pd.DataFrame):
    prices_api.save_df_to_file("sheets\\"+item_type, data)


if __name__ == "__main__":
    item_list = get_json("item_json_seperated.json")
    item_type_keyword = "_BAG"
    item_type = "Bags"
    get_and_save_item_types(item_type, item_type_keyword,
                            "Thetford", "1,2,3", item_list)
