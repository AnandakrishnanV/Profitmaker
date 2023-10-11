import pandas as pd
import json
import requests
from datetime import datetime, timedelta
import math
from openpyxl import load_workbook
import sys
sys.path.append('../Albion Scraper')
import albion_prices_helper as prices


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
        response_array = response_array + \
            call_albion_api(item, locations, qualities)
    return response_array


def format_response(response, df_hide):

    df_hide["buy_avg_prices"] = 0
    df_hide["buy_items_sold"] = 0
    df_hide["buy_days_totalled"] = 0
    df_hide["sell_avg_prices"] = 0
    df_hide["sell_items_sold"] = 0
    df_hide["sell_days_totalled"] = 0

    for item in response:
        days = len(item["data"]["prices_avg"])
        avg_prices = sum(item["data"]["prices_avg"])/days
        total_count = sum(item["data"]["item_count"])
        location = item["location"]
        item_id = item["item_id"]

        df_hide.loc[(df_hide["item_id"] == item_id) & (df_hide["city"] == location), [
            "buy_avg_prices", "buy_items_sold", "buy_days_totalled"]] = [avg_prices, total_count, days]

        df_hide.loc[(df_hide["item_id"] == item_id) & (df_hide["city"] == location), [
            "sell_avg_prices", "sell_items_sold", "sell_days_totalled"]] = [avg_prices, total_count, days]

    current_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    df_hide["buy_price_max_date"] = df_hide["buy_price_max_date"].str.replace(
        'T', ' ')

    df_hide["date"] = pd.to_datetime(
        df_hide["buy_price_max_date"], errors='coerce', format='%Y%m%d %H:%M:%S')

    def calc_time_diff(date):
        if pd.isnull(date):
            return None
        else:
            time_diff = abs(round((date-current_time) / timedelta(hours=1)))
            return str(time_diff) + " hours ago"

    df_hide["time_diff"] = df_hide["date"].apply(calc_time_diff)

    df_hide = df_hide.drop('date', axis=1)
    df_hide = df_hide.drop('buy_price_max_date', axis=1)
    df_hide = df_hide.drop('quality', axis=1)

    return df_hide


def get_hide_api(locations):
    item_list = prices.get_json("item_json_seperated.json")
    item_type_keyword = "_HIDE"
    item_type = "Material_Hide"
    location = locations
    qualities = None
    prices.get_and_save_item_types(
        item_type, item_type_keyword, location, qualities, item_list, True)


def hide_stats():
    df_hide = pd.read_excel("sheets\\Material_Hide.xlsx")

    book = load_workbook("sheets\\Material_Hide.xlsx")
    writer = pd.ExcelWriter("sheets\\Material_Hide.xlsx", engine='openpyxl')
    writer.book = book

    item_list = df_hide['item_id'].tolist()
    locations = "Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling"
    qualities = None
    response = get_from_api(item_list, locations, qualities)

    df_hide = format_response(response, df_hide)

    df_hide = df_hide.sort_values(['city', 'item_id'], ascending=[True, True])
    df_hide.to_excel(writer, sheet_name='Averages')

    print("Charts Retrieved...")

    cheapest_prices = df_hide.groupby(
        'item_id')['sell_price_min'].min().reset_index()
    cheapest_df = pd.merge(df_hide, cheapest_prices, on=[
        'item_id', 'sell_price_min'])

    cheapest_df = cheapest_df.sort_values(['item_id'], ascending=[True])

    cheapest_df.to_excel(writer, sheet_name='Cheapest')

    print("Cheapest Found..")

    expensive_prices = df_hide.groupby(
        'item_id')['sell_price_min'].max().reset_index()
    expensive_df = pd.merge(df_hide, expensive_prices, on=[
        'item_id', 'sell_price_min'])

    expensive_df = expensive_df.sort_values(['item_id'], ascending=[True])

    expensive_df.to_excel(writer, sheet_name='Expensives')
    writer.close()
    print("Expensives Found..")


if __name__ == "__main__":
    get_hide_api("Martlock,Bridgewatch,Lymhurst,Thetford,Fort Sterling")
    hide_stats()
