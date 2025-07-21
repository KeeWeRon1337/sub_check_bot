import os
import telegram
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "7305125772:AAFS7IxXWyKCGv9mg_Hx6VJO4XWRxlCESJc")
CHANNEL_USERNAME = "@foreign_advice"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Проверить подписку", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже, чтобы проверить подписку.", reply_markup=reply_markup)

# Кнопка
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            await context.bot.send_message(chat_id=user_id, text="✅ Подписка подтверждена!")
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ Вы не подписаны на канал.")
    except telegram.error.TelegramError:
        await context.bot.send_message(chat_id=user_id, text="❌ Не удалось проверить подписку.")

# Роут для webhook
@app.route("/", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Регистрация хендлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

if __name__ == "__main__":
    import asyncio
    from threading import Thread

    # Запуск Telegram приложения в отдельном потоке
    def run_telegram():
        application.run_polling()

    Thread(target=run_telegram).start()

    # Flask сервер
    app.run(port=10000, debug=True)
