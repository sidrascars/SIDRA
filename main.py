from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# استبدل 'YOUR_TOKEN' بالتوكن الحقيقي
TOKEN = "YOUR_TOKEN"

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
    updater.idle()

if __name__ == '__main__':
    main()
