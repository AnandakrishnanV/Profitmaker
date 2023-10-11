import json
import requests
import pandas as pd


def call_albion_api(items, locations, qualities):
    url = "https://east.albion-online-data.com/api/v2/stats/prices/"+items
    params = {
        "locations": locations if len(locations) else "Caerleon,Bridgewatch,Thetford,Lymhurst,Martlock,Fort Sterling",
        "qualities": qualities if qualities else None
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        json_data = json.dumps(data, indent=4)
        # print(json.dumps(data, indent=4))
        return json_data
    else:
        print("Request failed with status code:", response.status_code)

def return_df(data, sort_mats):
    df = pd.read_json(data)

    df = df.drop('sell_price_min_date', axis=1)
    df = df.drop('buy_price_min_date', axis=1)
    df = df.drop('buy_price_max_date', axis=1)
    df = df.drop('sell_price_max_date', axis=1)

    df = df.drop('sell_price_max', axis=1)
    df = df.drop('buy_price_min', axis=1)

    df = df.drop(df[(df['sell_price_min'] == 0)].index)

    df['Tier'] = df["item_id"].apply(
        lambda x: int((x.split("_")[0]).split("T")[1]))
    df['Enchant'] = df["item_id"].apply(
        lambda x: int(x.split("@")[1]) if len(x.split("@")) > 1 else 0)

    if sort_mats:
        df = df.sort_values(
            ['item_id', 'sell_price_min', 'city'], ascending=[True, True, True])
    else:
        df = df.sort_values(
            ['city', 'item_id', 'quality'], ascending=[True, True, True])

    return df

def save_df_to_file(item_path, data: pd.DataFrame):
    data.to_excel(item_path+".xlsx")
    

def save_to_file(item_type, data, sort_mats):
    df = pd.read_json(data)

    df = df.drop('sell_price_min_date', axis=1)
    df = df.drop('buy_price_min_date', axis=1)
    df = df.drop('sell_price_max_date', axis=1)

    df = df.drop('sell_price_max', axis=1)
    df = df.drop('buy_price_min', axis=1)

    df = df.drop(df[(df['sell_price_min'] == 0)].index)

    if (not sort_mats) :
        df['Tier'] = df["item_id"].apply(lambda x: int((x.split("_")[0]).split("T")[1]))
        df['Enchant'] = df["item_id"].apply(
            lambda x: int(x.split("@")[1]) if len(x.split("@")) > 1 else 0)

    if sort_mats:
        df = df.sort_values(
            ['item_id', 'sell_price_min', 'city'], ascending=[True, True, True])
    else:
        df = df.sort_values(
            ['city', 'item_id', 'quality'], ascending=[True, True, True])

    df.to_excel(item_type+".xlsx")
