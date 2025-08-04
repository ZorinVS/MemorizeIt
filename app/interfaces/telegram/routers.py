from fastapi import APIRouter, HTTPException

from app.application.use_cases.start_session import StartRepeatSessionUseCase
from app.domain.repositories import IUserRepository
from app.application.use_cases.telegram_start import TelegramStartUseCase
from app.application.use_cases.telegram_add_card import TelegramAddCardUseCase
# from app.application.use_cases.get_next_repeat_card import GetNextRepeatCardUseCase
# from app.domain.services.sessions.repeat_session_manager import SessionManagerDep
from app.infrastructure.repositories import UserRepository
from app.interfaces.telegram.types import StartBody, AddCardBody, DoRepeatBody, RepeatAnswerBody
from app.interfaces.telegram.deps import UserRepDep, CardRepDep, RepeatSessionRepDep

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/start")
async def telegram_start(
    data: StartBody,
    user_repo: UserRepDep,
):
    use_case = TelegramStartUseCase(user_repo)
    user = await use_case.execute(data)
    return {"message": "OK", "user_id": user.id}


@router.post("/add_card")
async def add_card(
    data: AddCardBody,
    user_repo: UserRepDep,
    card_repo: CardRepDep,
):
    use_case = TelegramAddCardUseCase(user_repo, card_repo)
    card = await use_case.execute(data)
    return {"message": "Card created", "card_id": card.id}


@router.post("/repeat/start")
async def repeat_start(
    data: DoRepeatBody,
    user_repo: UserRepDep,
    card_repo: CardRepDep,
    repeat_session_repo: RepeatSessionRepDep,
    # session_manager: SessionManagerDep,
):
    user = await user_repo.get_by_tg_id(data.tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    use_case = StartRepeatSessionUseCase(card_repo, repeat_session_repo, session_manager)
    count = await use_case.execute(user.id)
    return {"count": count}


# @router.post("/repeat/next")
# async def repeat_next(
#     data: DoRepeatBody,
#     user_repo: UserRepDep,
#     card_repo: CardRepDep,
#     repeat_session_repo: RepeatSessionRepDep,
#     session_manager: SessionManagerDep,
# ):
#     use_case = GetNextRepeatCardUseCase(user_repo, card_repo, repeat_session_repo, session_manager)
#     card = await use_case.execute(data.tg_id)
#
#     if not card:
#         raise HTTPException(status_code=404, detail="No card to repeat")
#
#     return {
#         "card_id": card.id,
#         "question": card.question,
#     }


# @router.post("/repeat/answer")
# async def repeat_answer(
#     data: RepeatAnswerBody,
#     user_repo: UserRepDep,
#     card_repo: CardRepDep,
#     session_manager: SessionManagerDep,
# ):
#     user = await user_repo.get_by_tg_id(data.tg_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     card = await card_repo.get_by_id(data.card_id)
#     if not card or card.user_id != user.id:
#         raise HTTPException(status_code=404, detail="Card not found")
#
#     # Обработка ответа
#     is_correct, is_finished = session_manager.submit_answer(
#         user_id=user.id,
#         card_id=card.id,
#         answer=data.answer,
#         correct_answer=card.answer
#     )
#
#     next_card_id = session_manager.get_next_card(user.id)
#
#     return {
#         "correct": is_correct,
#         "finished": is_finished,
#         "next_card_id": next_card_id,
#     }
