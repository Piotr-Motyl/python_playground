import requests

currency_type = "usd"
coins_list = None

def get_coins_list():
    response = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=true")
    # response format: {'id': '01coin', 'symbol': 'zoc', 'name': '01coin', 'platforms': {}}
    global coins_list
    if response.ok:
        data = response.json()
        print("*** response from Coingecko is OK (status 200) ***")
        coins_list = data

def find_coin_by_symbol(symbol):
    get_coins_list()
    symbol = symbol.lower().strip()
    for coin in coins_list:
        if coin["id"] == symbol:
            return coin
    else:
        return None

def get_coin_last_market(coin_id):
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=" + coin_id + "&vs_currencies=" + currency_type + "&include_market_cap=true&include_24hr_change=true&include_last_updated_at=true")
    #response format {'bitcoin': {'usd': 61117, 'usd_market_cap': 1207868931285.4607, 'usd_24h_change': -4.078211394230371, 'last_updated_at': 1727872027}}
    if response.ok:
        data = response.json()
        return data
    else:
        return None

def get_coin_price_in_currency(coin_id, currency_type):
    currency_type = currency_type.lower().strip()
    market_data = get_coin_last_market(coin_id)
    return market_data[coin_id][currency_type]