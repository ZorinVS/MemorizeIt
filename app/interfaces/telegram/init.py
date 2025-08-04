from app.interfaces.telegram.bot import bot, dp
from app.interfaces.telegram.handlers import router
from app.shared.config import settings


WEBHOOK_PATH = f"/bot/{settings.telegram_token}"
WEBHOOK_URL = f"{settings.ngrok_tunnel_url}{WEBHOOK_PATH}"


async def init_bot() -> None:
    """Инициализация Telegram-бота и установка webhook."""
    dp.include_router(router)
    webhook_info = await bot.get_webhook_info()

    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    print(f"Telegram webhook set to {WEBHOOK_URL}")


def get_webhook_path() -> str:
    return WEBHOOK_PATH
