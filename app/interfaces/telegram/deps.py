from typing import Annotated
from fastapi import Depends

from app.domain.repositories import IUserRepository, ICardRepository, IRepeatSessionRepository
from app.infrastructure.repositories import UserRepository, CardRepository, RepeatSessionRepository


# --- Функции-провайдеры ---
def get_user_repository() -> IUserRepository:
    return UserRepository()


def get_card_repository() -> ICardRepository:
    return CardRepository()


def get_repeat_session_repository() -> IRepeatSessionRepository:
    return RepeatSessionRepository()


# --- Типы для использования в эндпоинтах ---
UserRepDep = Annotated[IUserRepository, Depends(get_user_repository)]
CardRepDep = Annotated[ICardRepository, Depends(get_card_repository)]
RepeatSessionRepDep = Annotated[IRepeatSessionRepository, Depends(get_repeat_session_repository)]
