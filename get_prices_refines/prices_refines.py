import prices_cloth as cloth
import prices_leather as leather
import prices_metalbar as metalbar
import prices_planks as planks
import prices_stoneblock as stoneblock

import pandas as pd

import albion_prices_helper as prices


def get_prices():
    cloth.get_cloth("Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling")
    leather.get_leather("Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling")
    metalbar.get_metalbar("Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling")
    planks.get_planks("Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling")
    stoneblock.get_stoneblock("Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling")


def get_sheets():
    df_cloth = pd.read_excel("sheets\\Refined_Cloth.xlsx")
    df_leather = pd.read_excel("sheets\\Refined_Leather.xlsx")
    df_metalbar = pd.read_excel("sheets\\Refined_Metalbar.xlsx")
    df_planks = pd.read_excel("sheets\\Refined_Planks.xlsx")
    df_stoneblock = pd.read_excel("sheets\\Refined_Stoneblock.xlsx")

    return df_cloth, df_leather, df_metalbar, df_planks, df_stoneblock


def calculate_profits(refine: pd.DataFrame, very_profitable):
    cities = refine["city"].unique()
    items = refine["item_id"].unique()

    profits = []

    for item in items:
        for cityA in cities:
            for cityB in cities:
                if cityA != cityB and (item in refine.loc[refine['city'] == cityA, 'item_id'].values) and (item in refine.loc[refine['city'] == cityB, 'item_id'].values):
                    buy_price = refine.loc[(refine["item_id"] == item) & (
                        refine["city"] == cityA), "sell_price_min"].values[0]
                    sell_price = refine.loc[(refine["item_id"] == item) & (
                        refine["city"] == cityB), "sell_price_min"].values[0]
                    profit = sell_price - buy_price
                    if profit > 0:
                        percent_profit = int(profit/buy_price*100)
                        profits.append(
                            [item, cityA, cityB, buy_price, sell_price, profit, percent_profit])
                        if (profit >= 10 and percent_profit >= 15):
                            very_profitable.append(
                                [item, cityA, cityB, buy_price, sell_price, profit, percent_profit])

    profits_df = pd.DataFrame(profits, columns=[
                              'item_id', 'buy_city', 'sell_city', 'buy_price', 'sell_price', 'profit', 'percent_profit'])
    return profits_df


def save_to_file(profit, refine_type):

    profit.to_excel("profit_sheets\\"+refine_type+".xlsx")


def get_profitables():
    get_prices()

    print ("Prices retrieved")
    very_profitable = []

    refine_list = [df_cloth, df_leather, df_metalbar, df_planks, df_stoneblock] = get_sheets()
    for index, refine in enumerate(refine_list):
        type_index = ['Fibre', 'Wood', 'Ore', 'Rock', 'Hide']
        profits = calculate_profits(refine, very_profitable)
        save_to_file(profits, type_index[index])

    very_profitable_df = pd.DataFrame(very_profitable, columns=[
                                      'item_id', 'buy_city', 'sell_city', 'buy_price', 'sell_price', 'profit', 'percent_profit'])
    very_profitable_df = very_profitable_df.sort_values(
        ['buy_city', 'sell_city', 'profit'], ascending=[True, True, False])
    save_to_file(very_profitable_df, "Most_Profitable_Refines")


if __name__ == "__main__":
    get_profitables()
