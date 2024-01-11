import os
import json
import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, Updater
from dotenv import load_dotenv
import datetime
from hashnode import hashnode

load_dotenv()
TG_TOKEN = os.getenv('TOKEN')
PREFERENCE_FILE = os.getenv('PREFERENCE_FILE', 'user_preference.json')

# TODO: remove user preference

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
    user_inputs = ' '.join(user_inputs)
    if (len(user_inputs) < 1):
        await update.message.reply_text("Please provide a keyword")
        return
    user_id = str(update.message.from_user.id)
    preferences = load_preference()
    user_pref_list = []
    # user_pref_list.append(user_inputs)
    if user_id in preferences:
        user_pref = preferences[user_id]
        if user_inputs in user_pref:
            print('present')
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'{user_inputs} is already present'
            )
        else:
            print('not present')
            user_pref_list.append(user_inputs)
            user_pref = user_pref + user_pref_list
            preferences[user_id] = user_pref
    else:
        user_pref_list.append(user_inputs)
        preferences[user_id] = user_pref_list
    save_preference(preferences)
    user_pref_str = "\n".join(preferences[user_id])
    await update.message.reply_text(
            text=f'''
Your set preferences: 

*{user_pref_str}*
''', 
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )

def get_user_pref(user_id):
    preferences = load_preference()
    user_id = str(user_id)
    language = preferences.get(user_id)
    return language

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='''
Welcome to WFH Jobs Bot.
List of commands:
*/pref [keyword]*: Set New Preference.
*/config*: List your saved preferences.
*/sites*: List the sites which the bot is scraping.
'''
    )

async def sites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'''
Available sites:
*Hashnode*
''',
        parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
    )

async def get_hashnode_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = hashnode()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=jobs)
    return jobs

async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'BEEP {context.job.data}')
    hashnode_jobs = hashnode()
    user_id = context.job.user_id
    langs = get_user_pref(user_id)
    if hashnode_jobs is None:
        await context.bot.send_message(chat_id=context.job.chat_id, text='There are no jobs')
    elif langs is None:
        await context.bot.send_message(
            chat_id=context.job.chat_id, 
            text='No preferrence set. Please set a preference'
        )
    else:
        for lang in langs:
            if lang in hashnode_jobs:
                await context.bot.send_message(
                    chat_id=context.job.chat_id,
                    text=f'{lang} role open in Hashnode'
                )
            else:
                print('no keyword found')

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

async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pref = load_preference()
    user_pref = pref[str(update.effective_chat.id)]
    user_pref_str = "\n".join(user_pref)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'''
Your set preferences are: 

*{user_pref_str}*
            ''',
        parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
    )

async def remove_pref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = context.args
    user_input = ' '.join(user_input)
    pref = load_preference()
    user_id = str(update.effective_chat.id)
    user_pref = pref[user_id]
    if user_input in user_pref:
        user_pref.remove(user_input)
        pref[user_id] = user_pref
        save_preference(pref)
        user_pref_str = '\n'.join(user_pref)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'''
*{user_input}* has been removed from your preferences.
Your updated preferences are:

*{user_pref_str}*
                ''',
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{user_input} not found in your preferences.'
        )

def main() -> None:
    application = ApplicationBuilder().token(TG_TOKEN).build()
 
    # handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('hashnode', get_hashnode_jobs))
    application.add_handler(CommandHandler('pref', set_user_pref))
    application.add_handler(CommandHandler('config', config))
    application.add_handler(CommandHandler('timer', callback_timer))
    application.add_handler(CommandHandler('remove', remove_pref))
    application.add_handler(CommandHandler('sites', sites))

    application.run_polling()

if __name__ == "__main__":
    main()