import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router

# Upload data from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)

# Main function to start the bot
async def main():
    print("Bot successfully started and ready to work!")
    # Start polling (bot begins checking for new messages from Telegram servers)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Start the asynchronous event loop
    asyncio.run(main())