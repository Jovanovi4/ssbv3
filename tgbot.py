import logging
import telebot
from telebot import types



logging.basicConfig(level=logging.INFO)
token = "6342346052:AAEuN7u5QQS5ppkVyWCRbcLyxZWtg6-aKfI"
bot = telebot.TeleBot(token)


def telegram_bot(token, queue):
    # Функция ТЕЛЕГРАММБОТА
    all_results = []

    @bot.message_handler(commands=["start"])
    def start_message(message):
        # Создаем ReplyKeyboardMarkup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Начать')
        button_help = types.KeyboardButton('Помощь')
        markup.add(button_start, button_help)

        # Приветственное сообщение после команды /start
        welcome_text = "👋*Привет и добро пожаловать!*\n \n_Первым делом ознакомься с информацией о нашем боте_👇\nв разделе *'Помощь'*!\n"+"\n"
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

    @bot.message_handler(func=lambda message: True)
    def handle_buttons(message):
        if message.text == 'Начать':
            bot.send_message(message.chat.id, "Вы выбрали 'Начать'")
            while True:
                symbol_info = queue.get()
                try:
                    crypto = symbol_info.get("CRYPTO")
                    buy = symbol_info.get("Buy")
                    price_buy = symbol_info.get("Price buy")
                    size_buy = symbol_info.get("Size buy")
                    sell = symbol_info.get("Sell")
                    price_sell = symbol_info.get('Price sell')
                    size_sell = symbol_info.get('Size sell')
                    profit = round(symbol_info.get('Profit'), 3) if symbol_info.get('Profit') is not None else None

                    symbol_info_str = (
                        f"⚡ {crypto} ⚡\n"
                        f"------------------"+"\n"  
                        f"📗Покупать: {buy}\n"
                        f"➣Цена: {price_buy}$\n"
                        f"➣Объем: {size_buy}\n"+"\n"
                        f"📕Продавать: {sell}\n"
                        f"➣Цена: {price_sell}$\n"
                        f"➣Объем: {size_sell}\n"+"\n"
                        f"🔥Профит: {profit}%"
                    )
                    bot.send_message(message.chat.id, symbol_info_str, parse_mode="Markdown")
                       
                except Exception as e:
                    print(f"Ошибка при обработке данных: {e}")
                    pass
                if message.text.lower() == 'стоп':
                    bot.send_message(message.chat.id, "Вы остановили выдачу связок'")
                    break

        elif message.text == 'Помощь':
            bot.send_message(message.chat.id, """*Крипто-Арбитражный Бот Spread⚡Shock*

Добро пожаловать в мир криптовалютного арбитража с нашим умным ботом! 🚀

Что такое криптовалютный арбитраж?

Криптовалютный арбитраж - это стратегия торговли, при которой вы можете извлекать прибыль из разницы в ценах на одни и те же активы на различных биржах. Наш бот автоматизирует этот процесс, находя для вас выгодные сделки и предоставляя исчерпывающую информацию.

Основные возможности:

✅ *В реальном времени:* Получайте актуальные данные о самых выгодных сделках на разных биржах.

📈 *Анализ:* Подробная информация о том, где и когда покупать/продавать, чтобы максимизировать вашу прибыль.

🤖 *Автоматизация:* Бот работает 24/7, выявляя потенциальные сделки и отправляя уведомления, чтобы вы ничего не упустили.

💼 *Разнообразие бирж:* Поддерживается множество бирж, что позволяет вам выбирать оптимальные площадки для торговли.

📱 *Удобство через Telegram:* Вся информация доступна вам в вашем любимом мессенджере.

Нажмите кнопку *'Начать'* и Бот будет выдавать связки в реальном времени!""", parse_mode="Markdown")

    bot.polling()