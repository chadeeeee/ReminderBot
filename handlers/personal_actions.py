import logging 

from aiogram import executor, Dispatcher, Bot, types
import config
from aux_types import BotContext

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

async def start(message: types.Message):
    await message.answer("Привіт! Я бот👋\nЯ можу записувати твої нагадування\nЩоб дізнатися про мене більше напиши - /help. А щоб дізнатися про мене більше напиши - /info")

async def help(message: types.Message):
    await message.answer("Допомога\n\nЩоб запланувати нагадування просто напиши мені текст який має бути в нагадуванні🙂\nМої команди\n\n/start - запуск/перезапуск бота\n/help - допомога\n/developer - Інформація про розробника\n/donate - Підтримати проєкт")

async def info(message: types.Message):
    await message.answer("Інформація\nЦе бот з нагадуваннями. Я надіюся що бот буде оновлюватися і далі, тому чекайте версії 0.1.1(в ній буде додано купу всього😉) А я піду поїм вареників і буду думати як можна вдосконалити бота😉")

async def donate(message: types.Message):
    donate = "Підтримати проєкт можна за посиланням: <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>"
    await message.answer(donate, parse_mode="HTML", disable_web_page_preview=True)

async def version(message: types.Message):
    await message.answer("Версія боту - 0.0.1\nВерсія Python - 3.9.13\nВерсія Aiogram - 2.25.1")

async def code(message: types.Message):
    code = "Ось мій код на <a href='https://github.com/'>GitHub</a>"
    await message.answer(code, parse_mode="HTML", disable_web_page_preview=True)