import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, Updater
from dotenv import load_dotenv
import datetime
from hashnode import hashnode

load_dotenv()
TG_TOKEN = os.getenv('TOKEN')
PREFERENCE_FILE = os.getenv('PREFERENCE_FILE', 'user_preference.json')

# TODO: send the users message

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

async def set_user_pref(update: Update, context: CallbackContext):
    user_inputs = context.args
    if (len(user_inputs) < 1):
        await update.message.reply_text("provide a language")
        return
    user_id = str(update.message.from_user.id)
    preferences = load_preference()
    if user_id in preferences:
        user_pref = preferences[user_id]
        print(f'type of user_pref: {type(user_pref)}')
        # user_pref_set = set(user_pref)
        # print(f'user set in pref: {user_pref_set}')
        # user_pref  = list(user_pref_set)
        user_pref = user_pref + user_inputs
        print(f'user id in preference file: {user_pref}')
        preferences[user_id] = user_pref
    else:
        preferences[user_id] = user_inputs
        print('user id not in preference file')
    save_preference(preferences)
    await update.message.reply_text(f'preferred language: {context.args[0]}')

def get_user_pref(user_id):
    preferences = load_preference()
    user_id = str(user_id)
    language = preferences.get(user_id)
    print(f'lang in get_user_pref: {language}')
    return language

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to WFH Jobs Bot")

async def get_hashnode_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = hashnode()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=jobs)
    return jobs

async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'BEEP {context.job.data}')
    jobs = hashnode()
    user_id = context.job.user_id
    print(f'user_id: {user_id}')
    langs = get_user_pref(user_id)
    if jobs is None:
        await context.bot.send_message(chat_id=context.job.chat_id, text='There are no jobs')
    elif langs is None:
        await context.bot.send_message(
            chat_id=context.job.chat_id, 
            text='No preferrence set. Please set a preference'
        )
    else:
        for lang in langs:
            if lang in jobs:
                await context.bot.send_message(
                    chat_id=context.job.chat_id,
                    text=f'{lang} keyword found'
                )
            else:
                await context.bot.send_message(
                    chat_id=context.job.chat_id,
                    text='no keyword found'
                )

async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name = update.effective_chat.full_name
    # 8 hours = 28800 seconds
    context.job_queue.run_repeating(
        callback_alarm, 
        interval=28800, 
        first=1, 
        data=name, 
        chat_id=chat_id, 
        user_id=user_id
    )

def main() -> None:
    application = ApplicationBuilder().token(TG_TOKEN).build()

    # handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('hashnode', get_hashnode_jobs))
    application.add_handler(CommandHandler('set_pref', set_user_pref))
    # application.add_handler(CommandHandler('get_pref', get_user_pref))
    application.add_handler(CommandHandler('timer', callback_timer))

    application.run_polling()

if __name__ == "__main__":
    main()