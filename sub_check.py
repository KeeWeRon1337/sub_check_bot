import os
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

TOKEN = "7305125772:AAFS7IxXWyKCGv9mg_Hx6VJO4XWRxlCESJc"
CHANNEL_USERNAME = "@foreign_advice"  # укажи реальный юзернейм канала

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0)

# Стартовая команда
def start(update, context):
    keyboard = [[InlineKeyboardButton("🔍 Проверить подписку", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Нажми кнопку ниже, чтобы проверить подписку.", reply_markup=reply_markup)

# Обработка нажатия кнопки
def button(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    device = query.from_user.device if hasattr(query.from_user, 'device') else "неизвестно"

    try:
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            bot.send_message(chat_id=user_id, text=f"✅ Подписка подтверждена! Устройство: {device}")
            # Тут можно прикрепить файл: 
            # bot.send_document(chat_id=user_id, document=open("file.pdf", "rb"))
        else:
            bot.send_message(chat_id=user_id, text="❌ Вы не подписаны на канал.")
    except telegram.error.TelegramError:
        bot.send_message(chat_id=user_id, text="❌ Не удалось проверить подписку.")

    query.answer()

# Регистрация обработчиков
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))

# Обработка запроса от Telegram
@app.route("/", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Запуск
if __name__ == "__main__":
    app.run(debug=True)
