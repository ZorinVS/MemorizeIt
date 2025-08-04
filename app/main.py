from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot

from app.infrastructure.db.config import init_tortoise
from app.interfaces.telegram.bot import bot, dp
from app.interfaces.telegram.init import init_bot, get_webhook_path

WEBHOOK_PATH = get_webhook_path()


@asynccontextmanager
async def lifespan(application: FastAPI):
    await init_tortoise()
    await init_bot()
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    """Обработка входящих обновлений от Telegram (вебхук)."""
    update_dict = await request.json()
    print("✅ Webhook received:", update_dict)

    telegram_update = types.Update(**update_dict)
    await dp.feed_update(bot, telegram_update)

    return {"ok": True}


@app.get("/")
async def root():
    return {"message": "OK"}
