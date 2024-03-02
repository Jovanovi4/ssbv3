import logging
import asyncio
import aiohttp
import pandas as pd


async def create_ticker_info(exchange_name, symbol, bid, bid_size, ask, ask_size):
    # Функция создания DataFrame с данными от бирж
    data = {'Exchange': exchange_name, 'Symbol': symbol, 'Bid': bid, "Bid Size": bid_size , 'Ask': ask, "Ask Size": ask_size}
    return pd.DataFrame([data])


async def fetch_data(session, exchange_url, co, delay=0.02):
    # Функция передачи запросов с параметрами на биржи
    results = []

    result = await get_ticker_info(session, exchange_url, {"category": "spot", "coin":co, "symbol": co, "currency_pair": co, "instId": co, "type": "step0"})
    print(result)
    results.append(result)
    await asyncio.sleep(delay)  # Добавляем задержку между запросам
    return results


async def get_ticker_info(session, exchange_url, params):
    # Функция асинхронных запросов HTTP 
    try:
        async with session.get(exchange_url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f"Ошибка при запросе: {e}")
        return None
