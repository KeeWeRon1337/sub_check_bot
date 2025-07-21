import os
import threading
import asyncio
from flask import Flask, request

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "7305125772:AAFS7IxXWyKCGv9mg_Hx6VJO4XWRxlCESJc"
CHANNEL_USERNAME = "@foreign_advice"  # Укажи реальный username канала

# Flask-приложение
app = Flask(__name__)

# Создание Telegram приложения
application = ApplicationBuilder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Проверить подписку", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже, чтобы проверить подписку.", reply_markup=reply_markup)

# Обработка нажатия кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await context.bot.send_message(chat_id=user_id, text="✅ Подписка подтверждена!")
            # Можно отправить документ:
            # await context.bot.send_document(chat_id=user_id, document=open("file.pdf", "rb"))
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ Вы не подписаны на канал.")
    except Exception as e:
        await context.bot.send_message(chat_id=user_id, text="❌ Не удалось проверить подписку.")
        print(f"Ошибка проверки подписки: {e}")

# Обработка webhook-запросов от Telegram
@app.route("/", methods=["POST"])
def webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

# Функция запуска Telegram-бота (в потоке)
def run_telegram():
    asyncio.set_event_loop(asyncio.new_event_loop())
    application.run_polling()

# Запуск всего приложения
if __name__ == "__main__":
    # Запуск Telegram-бота в отдельном потоке
    threading.Thread(target=run_telegram).start()
    # Запуск Flask-приложения
    app.run(host="0.0.0.0", port=10000, debug=True)
