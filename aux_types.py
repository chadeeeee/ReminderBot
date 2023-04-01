import sqlite3
from dataclasses import dataclass

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


@dataclass
class BotContext:
    bot: Bot
    scheduler: AsyncIOScheduler
    connection: sqlite3.Connection
    # user_id: int
    admin_id: int
