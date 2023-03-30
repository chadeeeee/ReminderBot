import logging 

from aiogram import executor, Dispatcher, Bot, types
import config
from aux_types import BotContext

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

async def start(message: types.Message):
    await message.answer(f"Привіт, {message.from_user.full_name}! Я бот 👋\nЯ можу записувати твої нагадування 🔔\nЩоб дізнатися про мене більше напиши - /help")

async def help(message: types.Message):
    await message.answer("<b>Допомога</b>\n\nЩоб запланувати нагадування просто напиши мені текст який має бути в нагадуванні🙂\n<b>Мої команди</b>\n\n/start - запуск/перезапуск бота 🔄\n/help - допомога ⁉️\n/instruction - Інструкція як використовувати бота 📄\n/donate - Підтримати проект 💰\n/code - код бота ⌨\n/support - технічна підтримка ⚙️")

async def instruction(message: types.Message):
    await message.answer("<b>Інструкція по використанюю бота</b>\n1. Щоб запланувати нагадування, вам просто потрібно написати боту текст який має бути в нагадуванні\n2. Час потрібно вказувати без лишніх слів, типу: <code>час 2023-01-01 00:00</code>, а просто <code>2023-01-01 00:00</code>")

async def donate(message: types.Message):
    donate = "Підтримати проект можна за посиланням: <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a> 💰"
    await message.answer(donate, parse_mode="HTML", disable_web_page_preview=True)

async def version(message: types.Message):
    await message.answer("Версія боту - 1.0.0 🤖\nВерсія Python - 3.9.13 🐍\nВерсія Aiogram - 2.25.1 🇺🇦")

async def support(message: types.Message):
    await message.answer("⁉️ Якщо у тебе виникли якісь питання, або скарги - пишіть моєму розробнику - @infodevua_d")

async def code(message: types.Message):
    code = "Ось мій код на <a href='https://github.com/dpihovych/ReminderBot/'>GitHub</a> 🧑🏻‍💻"
    await message.answer(code, parse_mode="HTML", disable_web_page_preview=True)