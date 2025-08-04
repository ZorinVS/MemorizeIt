from aiogram import Bot, Dispatcher
from app.shared.config import settings
from aiogram.client.bot import DefaultBotProperties

bot = Bot(token=settings.telegram_token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
