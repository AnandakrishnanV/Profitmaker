import pandas as pd
import json
import requests
from datetime import datetime, timedelta
import math
import prices_refines as profitables

def split_to_fit(item_list):
    new_item_list = item_list
    no_of_items = len(new_item_list)
    total_size = len(",".join(new_item_list))

    divisor = int(no_of_items/math.ceil(total_size/3500))
    chunks = [new_item_list[x:x+divisor]
              for x in range(0, no_of_items, divisor)]

    str_chunks = []
    for chunk in chunks:
        str_chunks.append((",".join(chunk)))

    return str_chunks

def call_albion_api(items, locations, qualities):
    
    current_date = datetime.utcnow()
    date_format = "date="+(current_date-timedelta(days=1)).strftime('%m-%d-%Y') + \
        "&end_date="+current_date.strftime('%m-%d-%Y')

    url = "https://east.albion-online-data.com/api/v2/stats/charts/" + \
        items+".json?"+date_format+"&time-scale=24"
    params = {
        "locations": locations if len(locations) else "Caerleon,Bridgewatch,Thetford,Lymhurst,Martlock,Fort Sterling",
        "qualities": qualities if qualities else None
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()        
        return data
    else:
        print("Request failed with status code:", response.status_code)

def get_from_api(item_list, locations, qualities):
    split_item_list = split_to_fit(item_list)
    response_array = []

    for item in split_item_list:
        response_array = response_array + call_albion_api(item,locations,qualities)
    return response_array

def read_profitables_file(filename):
    df_profitables = pd.read_excel(filename)
    return df_profitables

def format_response(response, profitables_df):

    profitables_df["buy_avg_prices"] = 0
    profitables_df["buy_items_sold"] = 0
    profitables_df["buy_days_totalled"] = 0
    profitables_df["sell_avg_prices"] = 0
    profitables_df["sell_items_sold"] = 0
    profitables_df["sell_days_totalled"] = 0

    
    for item in response:
        days = len(item["data"]["prices_avg"])
        avg_prices = sum(item["data"]["prices_avg"])/days
        total_count = sum(item["data"]["item_count"])
        location = item["location"]
        item_id = item["item_id"]

        profitables_df.loc[(profitables_df["item_id"] == item_id) & (profitables_df["buy_city"] == location), [
            "buy_avg_prices", "buy_items_sold", "buy_days_totalled"]] = [avg_prices, total_count, days]
        
        profitables_df.loc[(profitables_df["item_id"] == item_id) & (profitables_df["sell_city"] == location), [
            "sell_avg_prices", "sell_items_sold", "sell_days_totalled"]] = [avg_prices, total_count, days]

def save_to_file(profitables, filename):
    profitables.to_excel("profit_sheets\\"+filename+".xlsx")

def get_charts():

    print ("Initiating Albion Money Maker!!")
    profitables.get_profitables()

    print ("Profitables Retrieved..")
    print ("Initiating Charts..")

    profitables_df = read_profitables_file(
        "profit_sheets\\Most_Profitable_Refines.xlsx")

    item_list = profitables_df['item_id'].tolist()
    locations = ""
    qualities = "1,2,3,4"
    response = get_from_api(item_list, locations, qualities)
    format_response(response, profitables_df)

    profitables_chart = profitables_df[(profitables_df["buy_days_totalled"]) != 0]
    save_to_file(profitables_chart, "Most_Profitable_Refines_Charts")

    new_df = profitables_df.loc[~((profitables_df['buy_days_totalled'] == 0) | (profitables_df['sell_days_totalled'] == 0)),:]
    save_to_file(new_df, "Most_Profitable_Refines_Charts_Strict")

    print ("Charts Retrieved...")
    print ("Program Complete, You did dope. GG")


def tests():
    current_date = datetime.utcnow()

    # date_format = "date="+current_date.strftime('%m-%d-%Y') + \
    #     "&end_date="+(current_date-timedelta(days=1)).strftime('%m-%d-%Y')

    # print(date_format)

    #  for item in response_data:
    #     avg_prices = sum(item["data"]["prices_avg"]) / \
    #         len(item["data"]["prices_avg"])
    #     total_count = sum(item["data"]["prices_avg"]["item_count"])

    #     break


if __name__ == "__main__":
    get_charts()

    # tests()
