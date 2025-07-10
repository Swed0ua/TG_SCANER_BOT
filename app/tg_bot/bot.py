import asyncio
import os
from aiogram import Bot, Dispatcher

from app.services.AuthHandler.auth_handler import AuthHandler

from app.services.SessionManagerService.session_manager_service import SessionManagerService
from app.services.SmartkasaService.smartkasa_service import SmartKasaService
from app.tg_bot.middlewares.auth import AuthMiddleware
from .handlers import router

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SMARTKASA_API_KEY = os.getenv('SMARTKASA_API_KEY')

smartkasa_service = SmartKasaService(api_key=SMARTKASA_API_KEY)
session_manager = SessionManagerService()

auth_handler = AuthHandler(session_manager, smartkasa_service)

async def start_tg_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp["auth_handler"] = auth_handler
    
    dp.update.middleware(AuthMiddleware(auth_handler))
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_tg_bot())