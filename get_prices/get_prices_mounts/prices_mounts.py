import get_prices_mounts as mounts


import pandas as pd
import json

import albion_prices_helper as prices


def get_json(filename):
    f = open(filename)
    return json.load(f)


def get_prices():
    mounts.get_mounts("Bridgewatch,Fort Sterling")
    print("Mounts Complete")


def get_sheets():
    df_mounts = pd.read_excel("sheets\\Mounts.xlsx")
    return [df_mounts]       # change it when adding more


def calculate_profits(equipment: pd.DataFrame, very_profitable, start_tier, end_tier, max_enchant, max_quality, start_location, item_json, key_index):
    equipment['id'] = equipment['item_id']
    cities = equipment["city"].unique()
    items = equipment["item_id"].unique()

    profits = []

    for item in items:
        for cityA in cities:
            for cityB in cities:
                if (item in equipment.loc[equipment['city'] == cityA, 'item_id'].values) and (item in equipment.loc[equipment['city'] == cityB, 'item_id'].values) and (start_location == "" or cityA == start_location):

                    itemid = item

                    item_name = item_json[key_index][itemid]["name"]

                    buy_price = equipment.loc[(equipment["item_id"] == item) & (
                        equipment["city"] == cityA), "sell_price_min"].values[0]
                    sell_price = equipment.loc[(equipment["item_id"] == item) & (
                        equipment["city"] == cityB), "sell_price_min"].values[0]

                    buy_price_at_city = equipment.loc[(equipment["item_id"] == item) & (
                        equipment["city"] == cityA), "buy_price_max"].values[0]
                    profit = sell_price - buy_price
                    profit_own_city = buy_price - buy_price_at_city
                    if profit > 0 and buy_price > 0 and sell_price > 0:
                        percent_profit = int(profit/buy_price*100)
                        profits.append(
                            [itemid, item_name, cityA, cityB, buy_price, sell_price, profit, percent_profit])
                        if (profit >= 1000 or percent_profit >= 10):
                            very_profitable.append(
                                [itemid, item_name, cityA, cityB, buy_price, sell_price, profit, percent_profit])
                    if profit_own_city > 100 and buy_price_at_city > 0 and buy_price > 0:
                        percent_profit_own_city = int(
                            profit/buy_price_at_city*100)
                        if (percent_profit_own_city >= 10):
                            # not adding to profits
                            very_profitable.append(
                                [itemid, item_name, cityA, cityA, buy_price_at_city, buy_price, profit_own_city, percent_profit_own_city])

    profits_df = pd.DataFrame(profits, columns=[
                              'item_id', 'item_name', 'buy_city', 'sell_city', 'buy_price', 'sell_price', 'profit', 'percent_profit'])
    return profits_df


def save_to_file(profit, equipment_type):

    profit.to_excel("profit_sheets\\"+equipment_type+".xlsx")


def get_profitables():
    print("Initiating Profitables...")
    print("Retreving Prices...")

    get_prices()

    print("Prices Retreived.")
    print("Calculating Profits")

    very_profitable = []
    item_json = get_json(
        "D:\Programming\Albion Scraper\item_json_seperated.json")

    equipment_list = get_sheets()
    for index, equipment in enumerate(equipment_list):
        type_index = ['Mounts']
        key_index = ["_MOUNT_"]
        profits = calculate_profits(
            equipment, very_profitable, 2, 7, 2, 4, "", item_json, key_index[index])
        save_to_file(profits, type_index[index])

    very_profitable_df = pd.DataFrame(very_profitable, columns=[
                                      'item_id', 'item_name', 'buy_city', 'sell_city', 'buy_price', 'sell_price', 'profit', 'percent_profit'])
    very_profitable_df = very_profitable_df.sort_values(
        ['buy_city', 'sell_city', 'profit'], ascending=[True, True, False])
    save_to_file(very_profitable_df, "Most_Profitable_Mounts")

    print("Calculated Most Profitables")


if __name__ == "__main__":
    get_profitables()
