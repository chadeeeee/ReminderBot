import logging
from contextlib import closing
from datetime import datetime
import pytz

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aux_types import BotContext


class States(StatesGroup):
    TEXT = State()
    DATE = State()


async def start(message: types.Message, bot_context: BotContext):
    await States.TEXT.set()


async def set_text(message: types.Message,
                   state: FSMContext,
                   bot_context: BotContext):
    async with state.proxy() as data:
        data['text'] = message.text.strip()
        if data['text']:
            await message.answer('Вкажіть дату і час нагадування в форматі "YYYY-MM-DD HH:MM"')
            await States.DATE.set()


async def set_date(message: types.Message, state: FSMContext, bot_context: BotContext):
    async with state.proxy() as data:
        try:
            date = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
            text = data['text']
            with closing(bot_context.connection.cursor()) as cursor:
                cursor.execute('INSERT INTO reminder (text, date) VALUES (?, ?)',
                               (text, date))
                job_id = cursor.lastrowid
                bot_context.connection.commit()
                logging.debug(f'{job_id=} {date=!s} "{text}"')

                bot_context.scheduler.add_job(send_message_to_admin,
                                              "date",
                                              run_date=date,
                                              timezone=(pytz.timezone('Europe/Kiev')),
                                              args=(job_id, bot_context))

            await message.reply("Ваше нагадування було встановлено успішно!")
            await States.TEXT.set()
        except ValueError as e:
            logging.exception(e)
            await message.answer('Некорректний формат дати.'
                                 'Вкажіть дату і час нагадування в форматі "YYYY-MM-DD HH:MM"')


async def send_message_to_admin(job_id: int, bot_context: BotContext):
    with closing(bot_context.connection.cursor()) as cursor:
        r = cursor.execute("SELECT text, date FROM reminder WHERE id=?", (job_id,))
        data = r.fetchone()
        text, date = data
        logging.debug(f'Job finished {job_id=} {date=!s} {text=}')

        await bot_context.bot.send_message(bot_context.admin_id, text)
