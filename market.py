import logging
import pandas as pd
# from main import *
from get_post import *



logging.basicConfig(level=logging.INFO)



async def spot_bybit(session, co, bybit_coin):
    # Получение тикеров с биржи Bybit
    exchange_name = 'Bybit'
    exchange_url = "https://api.bybit.com/v5/market/tickers"
    list_bybit = []

    results = await fetch_data(session, exchange_url, bybit_coin)

    for result in results:
        if result:
            try:
                for item in result["result"]["list"]:
                    symbol = co
                    bid = float(item["bid1Price"])
                    bid_size = float(item["bid1Size"])
                    ask = float(item["ask1Price"])
                    ask_size = float(item["ask1Size"])
                    ticker_info = await create_ticker_info(exchange_name, symbol, bid, bid_size, ask, ask_size)
                    list_bybit.append(ticker_info)
            except (KeyError, TypeError) as e:
            # Обработка ошибок, когда нет монеты на бирже
                pass
        else:
            pass
                    
    if list_bybit:
        return pd.concat(list_bybit, ignore_index=True)
    else:
        return pd.DataFrame()

async def spot_huobi(session, co, huobi_coin):
    # Получение тикеров с биржи Huobi
    exchange_name = 'Huobi'
    exchange_url = "https://api.huobi.pro/market/depth"
    list_huobi = []
    results = await fetch_data(session, exchange_url, huobi_coin, delay=0.02)

    for result in results:
        if result:
            try:
                symbol = co
                bid = float(result["tick"]["bids"][0][0])
                bid_size = float(result["tick"]["bids"][0][1])
                ask = float(result["tick"]["asks"][0][0])
                ask_size = float(result["tick"]["asks"][0][1])
                ticker_info = await create_ticker_info(exchange_name, symbol, bid, bid_size, ask, ask_size)        
                list_huobi.append(ticker_info)
            except (KeyError, TypeError) as e:
            # Обработка ошибок, когда нет монеты на бирже
                pass
        else:
            pass

    if list_huobi:
        return pd.concat(list_huobi, ignore_index=True)
    else:
        return pd.DataFrame()

async def spot_gateio(session, co, gateio_coin):
    # Получение тикеров с биржи Gate io
    exchange_name = 'Gate io'
    exchange_url = "https://api.gateio.ws/api/v4/spot/order_book"
    list_gateio = []

    results = await fetch_data(session, exchange_url, gateio_coin,)

    for result in results:
        if result:
            try:
                symbol = co
                bid = float(result["bids"][0][0])
                bid_size = float(result["bids"][0][1])
                ask = float(result["asks"][0][0])
                ask_size = float(result["asks"][0][1])
                ticker_info = await create_ticker_info(exchange_name, symbol, bid, bid_size, ask, ask_size)
                list_gateio.append(ticker_info)
            except (KeyError, TypeError) as e:
            # Обработка ошибок, когда нет монеты на бирже
                pass
        else:
            pass

    if list_gateio:
        return pd.concat(list_gateio, ignore_index=True)
    else:
        return pd.DataFrame()
    

async def spot_okx(session, co, okx_coin):
    # Получение тикеров с биржи Okx
    exchange_name = 'Okx'
    exchange_url = "https://www.okx.com/api/v5/market/books"
    list_okx = []

    results = await fetch_data(session, exchange_url, okx_coin, delay=0.02)
    for result in results:
        if result:
            try:
                symbol = co
                bid = float(result["data"][0]["bids"][0][0])
                bid_size = float(result["data"][0]["bids"][0][1])
                ask = float(result["data"][0]["asks"][0][0])
                ask_size = float(result["data"][0]["asks"][0][1])
                ticker_info = create_ticker_info(exchange_name, symbol, bid, bid_size, ask, ask_size)
                list_okx.append(ticker_info)

            except (KeyError, TypeError) as e:
            # Обработка ошибок, когда нет монеты на бирже
                pass
        else:
            pass

    if list_okx:
        return pd.concat(list_okx, ignore_index=True)
    else:
        return pd.DataFrame()
    
    
async def spot_okx(session, co, okx_coin):
    # Получение тикеров с биржи Okx
    exchange_name = 'Okx'
    exchange_url = "https://www.okx.com/api/v5/market/books"
    list_okx = []

    results = await fetch_data(session, exchange_url, okx_coin, delay=0.02)

    for result in results:
        if result["data"]:
            try:
                symbol = co
                bid3 = result["data"][0]["bids"]
                if bid3:
                    bid = float(bid3[0][0])
                    bid_size = float(result["data"][0]["bids"][0][1])
                    ask = float(result["data"][0]["asks"][0][0])
                    ask_size = float(result["data"][0]["asks"][0][1])
                    ticker_info = await create_ticker_info(exchange_name, symbol, bid, bid_size, ask, ask_size)
                    list_okx.append(ticker_info)
                else:
                    pass
            except (KeyError, TypeError) as e:
                # Обработка ошибок, когда нет монеты на бирже
                return None
        else:
            return None

    if list_okx:
        return pd.concat(list_okx, ignore_index=True)
    else:
        return pd.DataFrame()
    

async def spot_kucoin(session, co, kucoin_coin):
    # Получение тикеров с биржи Kukoin
    exchange_name = 'Kucoin'
    exchange_url = "https://api.kucoin.com/api/v1/market/orderbook/level1"
    list_kucoin = []

    results = await fetch_data(session, exchange_url, kucoin_coin)

    for result in results:
        if result:
            try:
                symbol = co
                bid = float(result["data"]["bestBid"])
                bid_size = float(result["data"]["bestBidSize"])
                ask = float(result["data"]["bestAsk"])
                ask_size= float(result["data"]["bestAskSize"])
                ticker_info = await create_ticker_info(exchange_name, symbol, bid,bid_size, ask, ask_size)
                list_kucoin.append(ticker_info)
            except (KeyError, TypeError) as e:
                # Обработка ошибок, когда нет монеты на бирже
                pass
        else:
            pass

    if list_kucoin:
        return pd.concat(list_kucoin, ignore_index=True)
    else:
        return pd.DataFrame()