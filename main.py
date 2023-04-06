import logging
import os.path
import sqlite3
from contextlib import closing
from datetime import datetime
from functools import partial

import tzlocal
from aiogram import executor, Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
from handlers.aux_types import BotContext
from handlers.personal_actions import start, help, donate, version, code, instruction, support  # info
from handlers.reminder import set_date, set_text, States


async def on_startup(dp: Dispatcher, bot_context: BotContext):
    now = datetime.now()
    logging.info(f'Startup {now:%Y-%m-%d %H:%M}')
    bot_context.scheduler.start()


def main():
    fmt = "[%(asctime)s] %(message)s (%(levelname)s) [%(name)s]"
    date_fmt = "%d.%m.%y %H:%M:%S"
    logging.basicConfig(level=logging.DEBUG, format=fmt, datefmt=date_fmt)
    for logger_name in ('asyncio', 'aiogram', 'apscheduler'):
        logging.getLogger(logger_name).setLevel(level=logging.WARNING)

    with sqlite3.connect("reminder.db") as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS reminder(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    text TEXT,
                    photo_id TEXT,
                    date DATETIME
                );""")

        scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)

        bot_context = BotContext(bot, scheduler, connection, config.ADMIN_ID)

        dp.register_message_handler(start, commands=['start'])
        dp.register_message_handler(help, commands=['help'])
        dp.register_message_handler(instruction, commands=['instruction'])
        dp.register_message_handler(support, commands=['support'])
        dp.register_message_handler(version, commands=['version'])
        dp.register_message_handler(donate, commands=['donate'])
        dp.register_message_handler(code, commands=['code'])

        dp.register_message_handler(
            partial(set_text, bot_context=bot_context),
            state=States.TEXT,
            content_types=types.ContentTypes.PHOTO | types.ContentTypes.TEXT
        )

        dp.register_message_handler(
            partial(set_text, bot_context=bot_context),
            state=None,
            content_types=types.ContentTypes.PHOTO | types.ContentTypes.TEXT
        )

        dp.register_message_handler(
            partial(set_date, bot_context=bot_context),
            state=States.DATE
        )
        executor.start_polling(dp,
                               skip_updates=True,
                               on_startup=partial(on_startup, bot_context=bot_context))


if __name__ == "__main__":
    main()
