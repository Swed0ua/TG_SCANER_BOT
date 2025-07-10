from aiogram.types import Update, Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


class AuthMiddleware(BaseMiddleware):
    def __init__(self, auth_handler):
        self.auth_handler = auth_handler

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        telegram_id = None

        if event.message and event.message.from_user:
            telegram_id = event.message.from_user.id
        elif event.callback_query and event.callback_query.from_user:
            telegram_id = event.callback_query.from_user.id
        else:
            print(f"[AuthMiddleware] Unsupported update type: {event}")
            return await handler(event, data)

        data["is_logged_in"] = self.auth_handler.is_logged_in(telegram_id)
        data["access_token"] = self.auth_handler.get_valid_access_token(telegram_id)

        return await handler(event, data)
