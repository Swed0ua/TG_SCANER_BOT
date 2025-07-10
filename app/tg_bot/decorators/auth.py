from functools import wraps
from aiogram.types import Message
from app.tg_bot.ui.messages import send_login_menu

def require_auth():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: Message, *args, **kwargs):
            auth_handler = kwargs.get("auth_handler")
            
            if not auth_handler:
                await send_login_menu(message)
                return
            if not auth_handler.is_logged_in(message.from_user.id):
                await send_login_menu(message)
                return
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator
