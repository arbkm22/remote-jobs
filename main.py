import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv

import config
from hashnode import hashnode

load_dotenv()
TG_TOKEN = os.getenv('TOKEN')

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

    application.run_polling()