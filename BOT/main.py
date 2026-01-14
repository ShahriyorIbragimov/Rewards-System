from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

DP = Dispatcher()


@DP.message(Command("start"))
async def command_start_handler(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton(
            text="🎓 Open Student App",
            web_app=WebAppInfo(url="https://chipper-zuccutto-0a2279.netlify.app/")
        )
    )
    await message.answer("Welcome!", reply_markup=keyboard)


async def main() -> None:
    BOT = Bot(token=os.getenv("API"))
    await DP.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
