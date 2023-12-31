import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext
from dotenv import load_dotenv

from hashnode import hashnode

load_dotenv()
TG_TOKEN = os.getenv('TOKEN')
PREFERENCE_FILE = os.getenv('PREFERENCE_FILE', 'user_preference.json')

def load_preference():
    try:
        with open (PREFERENCE_FILE, 'r') as file:
            file_content = file
            if not file_content:
                return {}
            else:
                data = json.load(file_content)
                return data
    except FileNotFoundError:
        return {}

# handle duplicate entries
def save_preference(preferences):
    with open(PREFERENCE_FILE, 'w') as file:
        json.dump(preferences, file, indent=4)

async def set_language(update: Update, context: CallbackContext):
    user_inputs = context.args
    if (len(user_inputs) < 1):
        await update.message.reply_text("provide a language")
        return
    user_id = update.message.from_user.id
    preferences = load_preference()
    preferences[user_id] = user_inputs
    save_preference(preferences)
    await update.message.reply_text(f'preferred language: {context.args[0]}')

async def get_language(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    preferences = load_preference()
    language = preferences.get(user_id)

    if language:
        await update.message.reply_text(f'preferred language: {language}')
    else:
        await update.message.reply_text(f'You do not have any preferred language set')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to WFH Jobs Bot")

async def get_hashnode_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = hashnode()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=jobs)

def get_user_preference(): 
    print('get user preference')

if __name__ == "__main__":
    application = ApplicationBuilder().token(TG_TOKEN).build()

    # handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('hashnode', get_hashnode_jobs))
    application.add_handler(CommandHandler('set_lang', set_language))
    application.add_handler(CommandHandler('get_lang', get_language))

    application.run_polling()