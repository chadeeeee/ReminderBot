import logging
from contextlib import closing
from datetime import datetime

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .aux_types import BotContext


class States(StatesGroup):
    TEXT = State()
    DATE = State()


async def start(message: types.Message, bot_context: BotContext):
    await States.TEXT.set()


async def set_text(message: types.Message,
                   state: FSMContext,
                   bot_context: BotContext):
    logging.debug(f"{message.content_type=}")

    if message.content_type == 'text':
        text = message.text
        photo_id = None
    else:  # if message.content_type == 'photo':
        text = message.caption
        photo_info = message.photo[-1]
        photo_id = photo_info.file_id

    logging.debug(f"Set {text=} {photo_id=}")

    async with state.proxy() as data:
        data['text'] = text
        data['photo_id'] = photo_id
        await message.answer('Вкажіть дату і час нагадування'
                             ' в форматі "YYYY-MM-DD HH:MM"')
        await States.DATE.set()


async def set_date(message: types.Message,
                   state: FSMContext,
                   bot_context: BotContext):
    async with state.proxy() as data:
        try:
            date = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
            text = data['text']
            photo_id = data['photo_id']
            with closing(bot_context.connection.cursor()) as cursor:
                cursor.execute('INSERT INTO reminder (user_id, text, photo_id, date) '
                               'VALUES (?, ?,?, ?)',
                               (message.from_user.id, text, photo_id, date))
                job_id = cursor.lastrowid
                bot_context.connection.commit()
                logging.debug(f'{job_id=} {date=!s} "{text} {photo_id=}"')

                bot_context.scheduler.add_job(send_message_to_admin,
                                              "date",
                                              run_date=date,
                                              timezone=(pytz.timezone('Europe/Kiev')),
                                              args=(job_id, bot_context))

            await message.reply("Ваше нагадування було встановлено успішно!")
            await state.reset_data()
            await States.TEXT.set()
        except ValueError as e:
            logging.exception(e)
            await message.answer('Некорректний формат дати.'
                                 'Вкажіть дату і час нагадування в форматі "YYYY-MM-DD HH:MM"')


async def send_message_to_admin(job_id: int, bot_context: BotContext):
    with closing(bot_context.connection.cursor()) as cursor:
        r = cursor.execute("SELECT user_id, text, photo_id, date "
                           "FROM reminder WHERE id=?", (job_id,))
        data = r.fetchone()
        user_id, text, photo_id, date = data
        logging.debug(f'Job finished {job_id=} {date=!s} {text=} {photo_id=}')

        if photo_id:
            await bot_context.bot.send_photo(user_id,
                                             caption=text,
                                             photo=photo_id)
        else:
            await bot_context.bot.send_message(user_id, text)
