from aiogram import Router, types
from aiogram.filters import CommandStart
from app.interfaces.telegram.deps import get_user_repository
from app.application.use_cases.telegram_start import TelegramStartUseCase
from app.interfaces.telegram.schemas import StartRequest

router = Router()


@router.message(CommandStart())
async def handle_start(msg: types.Message):
    user_repo = get_user_repository()
    use_case = TelegramStartUseCase(user_repo)

    req = StartRequest(
        tg_id=msg.from_user.id,
        first_name=msg.from_user.first_name,
        last_name=msg.from_user.last_name,
        username=msg.from_user.username,
    )

    await use_case.execute(req)
    await msg.answer(f"Привет, {msg.from_user.id}!")
