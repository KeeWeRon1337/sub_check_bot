from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = '7305125772:AAFS7IxXWyKCGv9mg_Hx6VJO4XWRxlCESJc'
CHANNEL_ID = '@foreign_advice'  # или ID (с -100 в начале)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    if member.status in ['member', 'administrator', 'creator']:
        # Пользователь подписан
        await update.message.reply_text("Спасибо за подписку! Вот ваш файл:")
        
        # Отправка файла (пример с PDF)
        with open("example.docx", "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename="example.docx"))
        
    else:
        # Пользователь не подписан
        await update.message.reply_text(
            f"Сначала подпишитесь на канал {CHANNEL_ID}, а затем нажмите /start снова."
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()