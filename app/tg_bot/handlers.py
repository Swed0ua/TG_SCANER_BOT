import asyncio
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
import tempfile
import os
import json

from app.services.InvoiceExtractor.invoice_extractor import InvoiceExtractor

router = Router()
OPENAI_API_KEY = os.getenv("OPENAI_KEY")
invoice_extractor = InvoiceExtractor(api_key=OPENAI_API_KEY)

async def process_invoice_image(message: Message, file_id: str, bot):
    file = await bot.get_file(file_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        await bot.download_file(file.file_path, destination=tmp)
        tmp_path = tmp.name

    loading_gif = "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3azNiN2F1MTVnMmsxaGN5YzU3ZXlnb2w0NjZobjlteWM4cHZyZTJvMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1n6FOu976kb1yr5uW5/giphy.gif" 
    loading_message = await message.answer_animation(loading_gif, caption="⏳ Сканую вашу накладну, зачекайте...")

    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, invoice_extractor.extract_invoice, tmp_path)
        await loading_message.delete()

        number = data.get("number", "—")
        date = data.get("date", "—")
        total = data.get("total", "—")
        supplier = data.get("supplier", {}).get("name", "—")

        main_text = (
            f"✅ <b>Дані накладної</b>\n"
            f"<b>Номер:</b> <code>{number}</code>\n"
            f"<b>Дата:</b> <code>{date}</code>\n"
            f"<b>Постачальник:</b> <code>{supplier}</code>\n"
            f"<b>Сума:</b> <code>{total}</code>\n"
            f"\n<pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>"
            )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Використати сканер ➕", callback_data="inDev")]
            ]
        )

        await message.answer(
            main_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        await loading_message.delete()
        await message.answer(f"❌ Сталася помилка при обробці: {e}")
    finally:
        os.remove(tmp_path)

# Handlers for commands and messages
async def start_handler(message: Message):
    await send_main_menu(message=message)

async def get_id_handler(message: Message):
    user_id = message.from_user.id
    formatted_message = f"""Ваш Telegram ID: <code>{user_id}</code>"""
    await message.answer(formatted_message, parse_mode=ParseMode.HTML)

async def handle_photo(message: Message):
    print(f"Received photo: {message.photo[-1].file_id}")
    photo = message.photo[-1]
    bot = message.bot
    await process_invoice_image(message, photo.file_id, bot)

async def handle_document(message: Message):
    document = message.document
    bot = message.bot
    if not document.mime_type.startswith("image/"):
        await message.answer("Будь ласка, надішліть саме зображення накладної (фото або файл).")
        return
    await process_invoice_image(message, document.file_id, bot)


async def send_main_menu(message:Message, is_new_mess:bool=True):

    menu_txt = f"😉 Вас вітає головне меню Бота\nТут ви можете отримати потрібну вам інформацію\n\n"
    keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
            [InlineKeyboardButton(text="Історія", callback_data=f"inDev")],
            [InlineKeyboardButton(text="Деталі", callback_data=f"inDev")]
        ])

    if is_new_mess:
        await message.answer(menu_txt, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await message.edit_text(menu_txt, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# Callback query handler for invoice processing
async def procc_callback_handler(callback: CallbackQuery):
    callback_data = callback.data 
    callback_list = callback_data.split("_")

    code = callback_list[0]
    if code == "inDev":
        await callback.answer(text="Функція в розробці 🛠", show_alert=True)

# Register the invoice processing handler
router.message.register(start_handler, Command("start"))
router.message.register(get_id_handler, Command("id"))

router.message.register(handle_photo, lambda msg: msg.photo)
router.message.register(handle_document, lambda msg: msg.document is not None)

router.callback_query.register(procc_callback_handler)