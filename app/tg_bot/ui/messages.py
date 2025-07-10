import os
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton, WebAppInfo
from aiogram.enums import ParseMode

LOGIN_UI_URL = os.getenv('LOGIN_UI_URL')

async def send_login_menu(message: Message):
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🔐 Натисніть щоб Увійти в кабінет",
                    web_app=WebAppInfo(url=LOGIN_UI_URL)
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("👋 Привіт, авторизуйтесь нижче!", reply_markup=keyboard, parse_mode=ParseMode.HTML)
