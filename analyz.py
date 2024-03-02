import logging
import pandas as pd
from queue import Queue



logging.basicConfig(level=logging.INFO)

    

def analyze_symbols(session, df_com, co, queue):
    """
    Анализирует данные о тикерах и вычисляет спред между биржами.

    Parameters:
    - session: объект сессии aiohttp.ClientSession.
    - df_com: DataFrame с данными о тикерах с разных бирж.
    - co: символ тикера.
    - queue: очередь для передачи данных между потоками.

    Returns:
    - symbol_info: информация о тикере и спреде между биржами.
    """
    # Фильтруем DataFrame по символу
    symbol_info = {}

    try:
        filtered_data = df_com[df_com['Symbol'] == co]
    except KeyError:   
        filtered_data = pd.DataFrame()
    
    if not filtered_data.empty:
            # Извлекаем информацию
            min_ask = filtered_data['Ask'].min()
            buy_exchange = filtered_data.loc[filtered_data['Ask'].idxmin(), 'Exchange']
            buy_size = filtered_data.loc[filtered_data['Ask'].idxmin(), 'Ask Size']

            max_bid = filtered_data['Bid'].max()
            sell_exchange = filtered_data.loc[filtered_data['Bid'].idxmax(), 'Exchange']
            sell_size = filtered_data.loc[filtered_data['Bid'].idxmin(), 'Bid Size']

            # Формула по которой высчитывается спред между биржами
            profit = (max_bid - min_ask) / (min_ask * 0.01)

            # Условия вывода гиперссылок на биржи с монетами
            if buy_exchange == "Bybit":
                link = co.replace("USDT", "/USDT")
                buy_link = f"https://www.bybit.com/en/trade/spot/{link}"

            elif buy_exchange == "Huobi":
                link = co.replace("USDT", "_USDT").lower()
                buy_link = f"https://www.htx.com/en-us/trade/{link}"

            elif buy_exchange == "Gate io":
                link = co.replace("USDT", "_USDT")
                buy_link = f"https://www.gate.io/ru/trade/{link}"

            elif buy_exchange == "Okx":
                link = co.replace("USDT", "-USDT").lower()
                buy_link = f"https://www.okx.com/ru/trade-spot/{link}"

            elif buy_exchange == "Kucoin":
                link = co.replace("USDT", "-USDT")
                buy_link = f"https://www.kucoin.com/ru/trade/{link}"                    
                        
            else:
                buy_link = "Exchange not found"

            if sell_exchange == "Bybit":
                link = co.replace("USDT", "/USDT")
                sell_link = f"https://www.bybit.com/en/trade/spot/{link}"

            elif sell_exchange == "Huobi":
                link = co.replace("USDT", "_USDT").lower()
                sell_link = f"https://www.htx.com/en-us/trade/{link}"

            elif sell_exchange == "Gate io":
                link = co.replace("USDT", "_USDT")
                sell_link = f"https://www.gate.io/ru/trade/{link}"

            elif sell_exchange == "Okx":
                link = co.replace("USDT", "-USDT").lower()
                sell_link = f"https://www.okx.com/ru/trade-spot/{link}"

            elif sell_exchange == "Kucoin":
                link = co.replace("USDT", "-USDT")
                sell_link = f"https://www.kucoin.com/ru/trade/{link}"                
            
            else:
                sell_link = "Exchange not found"

            # Разметка для гиперссылок
            markdown_buy = f"[{buy_exchange}]({buy_link})"
            markdown_sell = f"[{sell_exchange}]({sell_link})"

          # Сохраняем информацию в словаре
            if 1 < profit < 17:
                symbol_info = {"CRYPTO" : co,
                                     'Buy': markdown_buy,
                                     'Price buy': min_ask, 
                                     "Size buy": buy_size ,
                                     'Sell': markdown_sell, 
                                     'Price sell': max_bid, 
                                     "Size sell": sell_size, 
                                     'Profit': profit
                                     }
                queue.put(symbol_info) 
            else:
                logging.warning(f"No data found for symbol: {co}")

    return symbol_info
    

