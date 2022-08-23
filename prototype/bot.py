import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config

from app.handlers.common import register_handlers_common
from app.handlers.inline_int_book import inline_register_handlers_booking
from app.handlers.user_bookings import my_bookings_handlers_register
from app.handlers.main_menu import main_menu_start
from app.handlers.settings import admin_handler
from app.handlers.change_login import change_login_handlers_register


import database.db
import database.db_operations
from database.db_operations import DataBase

logger = logging.getLogger(__name__)
book = []


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/change_login", description="Изменить логин"),

    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    main_menu_start(dp)
    register_handlers_common(dp, config.tg_bot.admin_id)
    inline_register_handlers_booking(dp)
    my_bookings_handlers_register(dp)
    change_login_handlers_register(dp)
    admin_handler(dp)

    # database = DataBase()
    # a = database.select_unic_campus()

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
