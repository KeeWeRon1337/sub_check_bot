from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
import os

BOT_TOKEN = '7305125772:AAFS7IxXWyKCGv9mg_Hx6VJO4XWRxlCESJc'
CHANNEL_ID = '@foreign_advice'  # или ID (с -100 в начале)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Проверить подписку", callback_data="check_sub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Подпишитесь на наш канал и нажмите кнопку ниже 👇",
        reply_markup=reply_markup
    )

# Обработка кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    if member.status in ['member', 'administrator', 'creator']:
        # Подписан — отправим файл
        await query.edit_message_text("✅ Подписка подтверждена! Отправляю файл...")

        with open("example.docx", "rb") as f:
            await context.bot.send_document(chat_id=user_id, document=InputFile(f, filename="example.docx"))
    else:
        # Не подписан
        await query.edit_message_text(
            f"❌ Вы не подписаны на канал {CHANNEL_ID}.\n"
            f"Пожалуйста, подпишитесь и попробуйте снова."
        )

# Инициализация бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
