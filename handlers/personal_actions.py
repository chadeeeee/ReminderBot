from aiogram import Dispatcher, Bot, types

import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Привіт, {message.from_user.full_name}! Я бот 👋\n"
        f"Я можу записувати твої нагадування 🔔\n"
        f"Щоб дізнатися про мене більше напиши - /help")


# @dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        "<b>Допомога</b>\n\n"
        "Щоб запланувати нагадування просто"
        " напиши мені текст який має бути в нагадуванні🙂\n"
        "<b>Мої команди</b>\n\n"
        "/start - запуск/перезапуск бота 🔄\n"
        "/help - допомога ⁉️\n"
        "/instruction - Інструкція як використовувати бота 📄\n"
        "/donate - Підтримати проект 💰\n"
        "/code - код бота ⌨\n"
        "/support - технічна підтримка ⚙️")


# @dp.message_handler(commands=['instruction'])
async def instruction(message: types.Message):
    await message.answer(
        "<b>Інструкція по використаню бота</b>\n"
        "1. Щоб запланувати нагадування, вам просто потрібно "
        "написати боту текст який має бути в нагадуванні\n"
        "2. Час потрібно вказувати без лишніх слів, типу: "
        "<code>час 2023-01-01 00:00</code>, "
        "а просто <code>2023-01-01 00:00</code>")


# @dp.message_handler(commands=['donate'])
async def donate(message: types.Message):
    donate = "Підтримати проект можна за посиланням: " \
             "<a href='https://send.monobank.ua/jar/8N5ZfWFQJS'>monobank</a> 💰"
    await message.answer(donate,
                         parse_mode="HTML",
                         disable_web_page_preview=True)


# @dp.message_handler(commands=['version'])
async def version(message: types.Message):
    await message.answer("Версія боту - 1.0.0 🤖\n"
                         "Версія Python - 3.9.13 🐍\n"
                         "Версія Aiogram - 2.25.1 🇺🇦")


# @dp.message_handler(commands=['support'])
async def support(message: types.Message):
    await message.answer("⁉️ Якщо у тебе виникли якісь питання, "
                         "або скарги - пишіть моєму розробнику - @infodevua_d")


# @dp.message_handler(commands=['code'])
async def code(message: types.Message):
    code = "Ось мій код на " \
           "<a href='https://github.com/dpihovych/ReminderBot/'>GitHub</a> 🧑🏻‍💻"
    await message.answer(code,
                         parse_mode="HTML",
                         disable_web_page_preview=True)
