import os
from flask import Flask, request
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = '7305125772:AAFS7IxXWyKCGv9mg_Hx6VJO4XWRxlCESJc'
CHANNEL_ID = '@foreign_advice'  # или ID (с -100 в начале)
ADMIN_ID = int(os.getenv("@idk_whoisyou", "6305610953"))

# Команда /start
app = Flask(__name__)

# Создание Telegram-приложения
telegram_app = Application.builder().token(BOT_TOKEN).build()

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Проверить подписку", callback_data="check_sub")]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Подпишитесь на канал и нажмите кнопку ниже 👇", reply_markup=markup)

# Кнопка проверки подписки
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    if member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text("✅ Подписка подтверждена! Отправляю файл...")
        with open("example.docx", "rb") as f:
            await context.bot.send_document(chat_id=user_id, document=InputFile(f, filename="example.docx"))
    else:
        await query.edit_message_text(f"❌ Вы не подписаны на {CHANNEL_ID}. Подпишитесь и попробуйте снова.")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(check_subscription))

# Flask route для webhook
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok", 200

if __name__ == "__main__":
    url = os.getenv("https://sub-check-bot.onrender.com")
    if url:
        telegram_app.bot.set_webhook(url)
        print(f"✅ Webhook установлен: {url}")
    else:
        print("⚠️ Переменная https://sub-check-bot.onrender.com не задана, вебхук не установлен")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
