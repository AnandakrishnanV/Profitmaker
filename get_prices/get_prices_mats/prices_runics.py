import prices_runes as runes
import prices_relics as relics
import prices_souls as souls

import pandas as pd

import albion_prices_helper as prices


def get_prices():
    runes.get_wood("Martlock,Bridgewatch,Thetford")
    relics.get_ore("Martlock,Bridgewatch,Thetford")
    souls.get_hide("Martlock,Bridgewatch,Thetford")

def get_sheets():
    df_fibre = pd.read_excel("sheets\\Material_Fiber.xlsx")
    df_wood = pd.read_excel("sheets\\Material_Wood.xlsx")
    df_ore = pd.read_excel("sheets\\Material_Ore.xlsx")
    df_rock = pd.read_excel("sheets\\Material_Rock.xlsx")
    df_hide = pd.read_excel("sheets\\Material_Hide.xlsx")

    return df_fibre, df_wood, df_ore, df_rock, df_hide

def calculate_profits(mat: pd.DataFrame, very_profitable):
    cities = mat["city"].unique()
    items = mat["item_id"].unique()

    profits = []
    
    for item in items:
        for cityA in cities:
            for cityB in cities:
                if cityA != cityB and (item in mat.loc[mat['city'] == cityA, 'item_id'].values) and (item in mat.loc[mat['city'] == cityB, 'item_id'].values):
                    buy_price = mat.loc[(mat["item_id"] == item) & (mat["city"] == cityA), "sell_price_min"].values[0]
                    sell_price = mat.loc[(mat["item_id"] == item) & (mat["city"] == cityB), "sell_price_min"].values[0]
                    profit = sell_price - buy_price
                    if profit > 0:
                        percent_profit = int(profit/buy_price*100)
                        profits.append([item, cityA, cityB, buy_price, sell_price, profit, percent_profit])
                        if (profit >= 10 and percent_profit >= 15):
                            very_profitable.append([item, cityA, cityB, buy_price, sell_price, profit, percent_profit])

    profits_df = pd.DataFrame(profits, columns=['item_id', 'buy_city', 'sell_city', 'buy_price', 'sell_price', 'profit', 'percent_profit'])
    return profits_df

def save_to_file(profit, mat_type):

    profit.to_excel("profit_sheets\\"+mat_type+".xlsx")

def main():
    get_prices()
    very_profitable = []

    mat_list = [df_fibre, df_wood, df_ore, df_rock, df_hide] = get_sheets()
    for index, mat in enumerate(mat_list):
        type_index = ['Fibre', 'Wood', 'Ore', 'Rock', 'Hide']
        profits = calculate_profits(mat, very_profitable)
        save_to_file(profits, type_index[index])
    
    very_profitable_df = pd.DataFrame(very_profitable, columns=['item_id', 'buy_city', 'sell_city', 'buy_price', 'sell_price', 'profit', 'percent_profit'])
    save_to_file(very_profitable_df, "Most_Profitable")

main()
