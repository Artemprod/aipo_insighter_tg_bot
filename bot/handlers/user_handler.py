from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.service import validate_youtube_url
from web.api.exteranl_databse_queries import get_transcribed_text, get_summary_text, do_youtube_transcribition
from web.nats_listener.listener import received_transcribed_id, received_summary_id
from pprint import pprint
router = Router()


async def generate_text_file(content: str) -> tuple:
    file_name = f'Документ от {datetime.now().strftime("%d %B %Y")}.txt'
    # Кодируем содержимое в байты
    file_bytes = content.encode("utf-8")
    return file_bytes, file_name

@router.callback_query(F.data == '')
async def processed_show_all_assistants(callback: CallbackQuery, ):
    ...

# сценарий обработки ютуб
# 1 Получить данные от пользователя
# 2 отправить даннее через api запрос
# 3 Дождаться сообщения что результат 1 готов ( трансрикбированый ткс )
# 4 если текс готов то отправить запрос в воркер чтобы он отдал текст
# 5 выдать пользователю текст
# 6 дождаться сообщения что самари текст гтов
# 7 если готв запросить из воркера текст саммари
# 8 отдать текст текст пользователю

# сценарий обработки из хранилища
# тоже самое только разные эндпоинтов



@router.message(F.content_type.in_({ContentType.TEXT}))
async def processed_load_youtube_file(message: Message,bot:Bot):
    income_text = message.text
    is_youtube = await validate_youtube_url(income_text)
    if not is_youtube:
        await message.answer(text="Это не ютуб ссылка")
    else:
        await do_youtube_transcribition(youtube_url=income_text)
        text_id = await received_transcribed_id()
        # возможно подумать сделать text_id = await async.create_task(received_transcribed_id())
        transcribed_text = await get_transcribed_text(text_id=text_id)
        if not transcribed_text:
            await message.answer(text="Нету текста")
        else:
            file_in_memory, file_name = await generate_text_file(
                content=transcribed_text,

            )
            await bot.send_document(
                chat_id=message.chat.id,
                document=BufferedInputFile(file=file_in_memory, filename=file_name))
        summary_id = await received_summary_id()
        summary = await get_summary_text(text_id=summary_id)
        if not summary:
            await message.answer(text="Нету саммари текста")
        else:
            await message.answer(text=summary)





# @router.message()
# async def all_messages(message: Message,bot:Bot):


# @router.callback_query(lambda c: 'source:NATS' in c.data)
# async def handle_query(query: CallbackQuery):
#     # Ваша логика обработки
#     print(query)
#     await query.answer('Это сообщение от сервиса NATS')