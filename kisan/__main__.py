import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pyrogram import Client
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token, API_ID, and API_HASH from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
API_ID = os.getenv("API_ID", "YOUR_API_ID")
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID", "YOUR_OWNER_ID"))

# Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your ban-all bot.')

def ban_all(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    bot = context.bot

    # Check if the user running the command is the owner
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("You are not authorized to run this command.")
        return

    # Get all chat members
    for member in bot.get_chat_members(chat_id):
        user_id = member.user.id

        # Don't ban the bot itself and the owner
        if user_id == bot.id or user_id == OWNER_ID:
            continue

        try:
            bot.ban_chat_member(chat_id, user_id)
            logger.info(f"Banned user {user_id}")
        except Exception as e:
            logger.error(f"Error banning user {user_id}: {e}")

    update.message.reply_text("Banned all members.")

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("banall", ban_all))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
