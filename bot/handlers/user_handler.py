from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.service import validate_youtube_url
from web.api.exteranl_databse_queries import get_transcribed_text, get_summary_text, do_youtube_transcribition
from web.nats_listener.listener import received_result

router = Router()


@router.callback_query(F.data == '')
async def processed_show_all_assistants(callback: CallbackQuery, ):
    ...


@router.message(F.content_type.in_({ContentType.TEXT}))
async def processed_load_youtube_file(
        message: Message,
):
    income_text = message.text
    is_youtube = await validate_youtube_url(income_text)
    if not is_youtube:
        await message.answer(text="Это не ютуб ссылка")
    else:
        await do_youtube_transcribition(youtube_url=income_text)
        text_id = await received_result()
        print(text_id)
        if text_id:
            transcribed_text = await get_transcribed_text(text_id=text_id)
            print(transcribed_text)
            await message.answer(text=transcribed_text)

