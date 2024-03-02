import logging
import asyncio
import aiohttp
import pandas as pd
from tickers import coins
import threading
from queue import Queue
import time
from market import*
from analyz import analyze_symbols
from tgbot import *


logging.basicConfig(level=logging.INFO)


async def main(queue):
    """
    Основная функция для получения данных с бирж и их анализа.

    Parameters:
    - queue: очередь для передачи данных между потоками.

    Returns:
    - symbol_info: информация о тикерах с разных бирж.
    """

    # Список для хранения результатов всех бирж
    symbol_info = {}
    
    # Цикл обработки текста для GET запросов на биржи
    for co in coins:
        bybit_coin = co
        huobi_coin = co.lower()
        gateio_coin = co.replace("USDT", "_USDT")
        okx_coin = co.replace("USDT", "-USDT")
        kucoin_coin = co.replace("USDT", "-USDT")

        async with aiohttp.ClientSession() as session:
            bybit = spot_bybit(session, co, bybit_coin)
            huobi = spot_huobi(session, co, huobi_coin)   
            gateio = spot_gateio(session, co, gateio_coin)
            okx = spot_okx(session, co, okx_coin)   
            kucoin = spot_kucoin(session, co, kucoin_coin)

             # Дождемся завершения всех запросов
            bybit, huobi, gateio, okx, kucoin = await asyncio.gather(bybit, huobi, gateio, okx, kucoin)

            # Объединим результаты в один датафрейм
        df_com = pd.concat([bybit, huobi, gateio, okx, kucoin], ignore_index=True)
        symbol_info = analyze_symbols(session, df_com, co, queue)
        
    return symbol_info


def run_main_loop(queue):
    """
    Запускает цикл событий asyncio в отдельном потоке.

    Parameters:
    - queue: очередь для передачи данных между потоками.
    """

    # Функция создания нового цикла событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(periodic_main(queue))
    finally:
        loop.close()


async def periodic_main(queue):
    """
    Периодический запуск основной функции.

    Parameters:
    - queue: очередь для передачи данных между потоками.
    """
    # Функция переодического запуска запросов
    while True:
        await main(queue)
        time.sleep(2806)


if __name__ == "__main__":
    # Создаем объект очереди
    data_queue = Queue()
    
    # Запускаем потоки
    symbol_info_thread = threading.Thread(target=run_main_loop, args=(data_queue,))
    thread2 = threading.Thread(target=telegram_bot, args=(token, data_queue))
    symbol_info_thread.start()
    thread2.start()

    # Ждем завершения потоков
    symbol_info_thread.join()
    thread2.join()