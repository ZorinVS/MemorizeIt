from aiogram import Router
from app.interfaces.telegram.handlers import start, add_card

router = Router()
router.include_router(start.router)
# router.include_router(add_card.router)
