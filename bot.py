# _____ADMIN BOT
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from bot.config.bot_configs import load_bot_config
from bot.handlers import command_handler, user_handler
from bot.keyboards.main_menu import set_main_menu

config = load_bot_config('.env')


async def main() -> None:
    session = AiohttpSession(api=TelegramAPIServer.from_base(
        config.AdminBot.telegram_server_url
    ))

    bot: Bot = Bot(
        token=config.AdminBot.tg_bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
        # session=session
    )

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
