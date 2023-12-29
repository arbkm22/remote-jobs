import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import config
from hashnode import hashnode

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to WFH Jobs Bot")

async def get_hashnode_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = hashnode()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=jobs)


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    hashnode_handler = CommandHandler('hashnode', get_hashnode_jobs)
    application.add_handler(hashnode_handler)

    application.run_polling()