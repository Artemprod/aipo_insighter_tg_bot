import os.path
from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message, BufferedInputFile

from bot.config.bot_configs import load_bot_config
from bot.models.start_process import StartFromYouTubeMessage, StartFromS3Message
from bot.s3.selectel_api.s3_client import S3Client
from bot.service import validate_youtube_url
from bot.utils import get_file_url
from web.api.exteranl_databse_queries import get_transcribed_text, get_summary_text, do_youtube_transcribition, \
    do_s3_transcribtion
from web.nats_listener.listener import received_transcribed_id

router = Router()
config = load_bot_config('.env')


async def generate_text_file(content: str) -> tuple:
    file_name = f'Документ от {datetime.now().strftime("%d %B %Y")}.txt'
    # Кодируем содержимое в байты
    file_bytes = content.encode("utf-8")
    return file_bytes, file_name


@router.callback_query(F.data == '')
async def processed_show_all_assistants(callback: CallbackQuery, ):
    ...


@router.message(F.content_type.in_({ContentType.TEXT}))
async def processed_load_youtube_file(message: Message, bot: Bot):
    income_text = message.text
    is_youtube = await validate_youtube_url(income_text)
    if not is_youtube:
        await message.answer(text="Это не ютуб ссылка")
    else:
        await do_youtube_transcribition(StartFromYouTubeMessage(
            user_id=message.from_user.id,
            youtube_url=income_text,
            assistant_id=3,
            publisher_queue="telegram.wait",
            source="telegram",
        ))
        # await message.answer(text='Делаем summery')
        text_id = await received_transcribed_id()
        # возможно подумать сделать text_id = await async.create_task(received_transcribed_id())
        transcribed_text = await get_transcribed_text(text_id=text_id, )
        if not transcribed_text:
            await message.answer(text="Нету текста")
        else:
            file_in_memory, file_name = await generate_text_file(
                content=transcribed_text,

            )
            await bot.send_document(
                chat_id=message.chat.id,
                document=BufferedInputFile(file=file_in_memory, filename=file_name))

        summary_id = await received_transcribed_id()

        summary = await get_summary_text(text_id=summary_id, )

        if not summary:
            await message.answer(text="Нету саммари текста")
        else:
            await message.answer(text=summary)


@router.message(F.document)
async def document_handler(message: Message, bot: Bot):
    document_data = message.document

    file_url = await get_file_url(document_data.file_id)
    print(file_url)

    # Скачиваем файл с телеграм сервера
    await bot.download_file(
        file_path=file_url,
        destination=f'F:\\PycharmProjects\\aipo_insighter_tg_bot\\downloads\\{document_data.file_name}'
    )

    s3_client = S3Client(
        access_key=config.s3_config.access_key,
        secret_key=config.s3_config.secret_key,
        endpoint_url="https://s3.storage.selcloud.ru",
        bucket_name="private-insighter-1",
    )
    # Загружаем файл в S3
    # print(temp_file_path)
    if os.path.exists(f"F:\\PycharmProjects\\aipo_insighter_tg_bot\\downloads\\{document_data.file_name}"):
        object_name = await s3_client.upload_file(
            f"F:\\PycharmProjects\\aipo_insighter_tg_bot\\downloads\\{document_data.file_name}")

    # Генерируем временную ссылку для загруженного файла
    presigned_url = await s3_client.generate_presigned_url(object_name)

    # Отправляем пользователю ссылку
    transcribed_text = await do_s3_transcribtion(
        StartFromS3Message(
            user_id=message.from_user.id,
            s3_path=presigned_url,
            assistant_id=3,
            publisher_queue='telegram.wait',
        )
    )

    # await message.answer(text='Делаем summery')
    text_id = await received_transcribed_id()
    transcribed_text = await get_transcribed_text(text_id=text_id, )
    if not transcribed_text:
        await message.answer(text="Нету текста")
    else:
        file_in_memory, file_name = await generate_text_file(
            content=transcribed_text,

        )
        await bot.send_document(
            chat_id=message.chat.id,
            document=BufferedInputFile(file=file_in_memory, filename=file_name))

    summary_id = await received_transcribed_id()

    summary = await get_summary_text(text_id=summary_id, )

    if not summary:
        await message.answer(text="Нету саммари текста")
    else:
        await message.answer(text=summary)
