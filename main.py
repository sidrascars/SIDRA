import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
import nest_asyncio
import asyncio
import requests

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
BOT_URL = os.environ.get("BOT_URL")  # رابط موقعك في Render مثل: https://black-daftar-bot.onrender.com

CHOOSING, TYPING_CONFESSION, AFTER_CONFESSION, CHOOSING_EXERCISE, TYPING_EXERCISE = range(5)

confessions_storage = []
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbyMmr-a_dDJtbGm3ZZ3x1yDPi3arGghpU9jLh1ZqYe8Pnbj4CTxKtPY3rZp9MaYOoCP1w/exec"

async def send_to_sheet(entry_type, content):
    try:
        requests.post(GOOGLE_SHEET_URL, json={"type": entry_type, "content": content})
    except:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("ارسلي اعترافًا", callback_data="confess")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🖤 مرحبًا بكِ في دفترها الأسود", reply_markup=reply_markup)
    return CHOOSING

async def confess_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("📩 اكتبي اعترافك الآن...")
    return TYPING_CONFESSION

async def received_confession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    confessions_storage.append(text)
    await send_to_sheet("اعتراف", text)
    await update.message.reply_text("🖤 تم استقبال اعترافك.")
    return ConversationHandler.END

@app.route("/")
def index():
    return "✅ البوت يعمل عبر Webhook"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app.bot.bot)
    asyncio.run(app.bot.process_update(update))
    return "OK"

async def run_bot():
    if not TOKEN or not BOT_URL:
        print("❗ BOT_TOKEN أو BOT_URL غير موجودين")
        return

    application = Application.builder().token(TOKEN).build()
    app.bot = application

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [CallbackQueryHandler(confess_handler)],
            TYPING_CONFESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_confession)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    # إعداد Webhook
    await application.bot.set_webhook(url=f"{BOT_URL}/{TOKEN}")
    print("✅ Webhook مُفعل على:", f"{BOT_URL}/{TOKEN}")

nest_asyncio.apply()
asyncio.run(run_bot())
