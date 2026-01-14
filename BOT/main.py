from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo

bot = Bot(token="BOT_TOKEN")
dp = Dispatcher()

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton(
            text="🎓 Open Student App",
            web_app=WebAppInfo(url="https://your-react-app.com")
        )
    )
    await msg.answer("Welcome!", reply_markup=keyboard)
