
import asyncio
from dotenv import load_dotenv

load_dotenv()

from app.tg_bot.bot import start_tg_bot


if __name__ == "__main__":
    asyncio.run(start_tg_bot())