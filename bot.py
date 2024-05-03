# _____ADMIN BOT
import asyncio
import os.path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import Redis, RedisStorage

from bot.handlers import command_handler, user_handler
from bot.keyboards.main_menu import set_main_menu


async def main() -> None:
    # config = config_data

    # redis = Redis(host=config.redis_storage.admin_bot_docker_host,
    #               port=config.redis_storage.admin_bot_docker_port)
    # storage: RedisStorage = RedisStorage(redis=redis)

    bot: Bot = Bot(token="6145823156:AAElAEKBthci1mgd4mk1GX7VbDqMYUnbqEA",
                   default=DefaultBotProperties(parse_mode="HTML"))

    # Добовляем хэгдлеры в диспечтер через роутеры
    dp: Dispatcher = Dispatcher()
    dp.include_router(command_handler.router)
    dp.include_router(user_handler.router)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем прослушку бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(main())
