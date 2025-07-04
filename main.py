import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask 
TOKEN = os.environ.get('TOKEN')
app = Flask(__name__)  

@app.route('/')  
def home():
    return "Bot is running!"  

def start(update: Update, context: CallbackContext):
    update.message.reply_text('مرحبًا! أنا بوت تيليجرام يعمل على Render! 🚀')

def echo(update: Update, context: CallbackContext):
    user_text = update.message.text
    update.message.reply_text(f'لقد قلت: {user_text}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    
    # أضف هذه الأسطر لتشغيل Flask مع البوت
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    updater.idle()

if __name__ == '__main__':
    main()
