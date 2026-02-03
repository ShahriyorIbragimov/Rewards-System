from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def main() -> None:
    token = os.getenv("API")
    if not token:
        raise ValueError("API token not found in environment variables")
    
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    @dp.message(Command("start"))
    async def command_start_handler(message: types.Message) -> None:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="👛 View Balance"
                    )
                ]
            ],
            resize_keyboard=True
        )

        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎓 Start App",
                        web_app=WebAppInfo(url="https://utterly-fancy-gator.ngrok-free.app")
                    )
                ]
            ]
        )

        await message.answer(
            text="Welcome to Rewards System! 🎉",
            reply_markup=keyboard
        )
        
        await message.answer(
            "Press the button to continue:",
            reply_markup=inline_keyboard
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


