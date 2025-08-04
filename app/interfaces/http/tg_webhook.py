from fastapi import APIRouter, Request, Header
from app.shared.config import settings
from app.interfaces.telegram.bot import dp, bot

router = APIRouter()


@router.post(settings.webhook_path)
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None)
):
    if x_telegram_bot_api_secret_token != settings.webhook_secret:
        return {"status": "unauthorized"}

    body = await request.body()
    await dp.feed_webhook_update(bot=bot, update=body)
    return {"status": "ok"}
