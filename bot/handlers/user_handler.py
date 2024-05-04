from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.service import validate_youtube_url
from web.api.exteranl_databse_queries import get_transcribed_text, get_summary_text, do_youtube_transcribition
from web.nats_listener.listener import received_result
from pprint import pprint
router = Router()


@router.callback_query(F.data == '')
async def processed_show_all_assistants(callback: CallbackQuery, ):
    ...


@router.message(F.content_type.in_({ContentType.TEXT}))
async def processed_load_youtube_file(message: Message,):
    income_text = message.text
    is_youtube = await validate_youtube_url(income_text)
    if not is_youtube:
        await message.answer(text="Это не ютуб ссылка")
    else:
        await do_youtube_transcribition(youtube_url=income_text)
        text_id = await received_result()
        transcribed_text = await get_transcribed_text(text_id=text_id)
        print(transcribed_text)
        await message.answer(text=transcribed_text)




# @router.message()
# async def all_messages(message: Message,bot:Bot):


# @router.callback_query(lambda c: 'source:NATS' in c.data)
# async def handle_query(query: CallbackQuery):
#     # Ваша логика обработки
#     print(query)
#     await query.answer('Это сообщение от сервиса NATS')