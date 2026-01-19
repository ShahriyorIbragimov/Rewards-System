from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import asyncio
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize bot and dispatcher
async def main() -> None:
    token = os.getenv("API")
    if not token:
        raise ValueError("API token not found in environment variables")
    
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Define handlers
    @dp.message(Command("start"))
    async def command_start_handler(message: types.Message) -> None:
        # Create inline buttons with web_app
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎓 Admin App",
                        web_app=WebAppInfo(url="https://rewards-system.netlify.app/admin")
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👨‍🎓 Student App",
                        web_app=WebAppInfo(url="https://rewards-system.netlify.app/student")
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👨‍🏫 Teacher App",
                        web_app=WebAppInfo(url="https://rewards-system.netlify.app/teacher")
                    )
                ]
            ]
        )
        await message.answer(
            "Welcome to Rewards System! 🎉\n\n"
            "Choose your role to continue:",
            reply_markup=keyboard
        )

    @dp.message(Command("help"))
    async def command_help_handler(message: types.Message) -> None:
        await message.answer(
            "Available commands:\n"
            "/start - Show available apps\n"
            "/help - Show this help message"
        )

    try:
        logger.info("Bot started polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())


