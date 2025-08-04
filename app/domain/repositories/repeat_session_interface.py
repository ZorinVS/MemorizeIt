from typing import Protocol
from app.domain.models import RepeatSession, RepeatSessionCard


class IRepeatSessionRepository(Protocol):
    async def get_active_session(self, user_id: int) -> RepeatSession | None:
        """Получить активную сессию пользователя"""
        ...

    async def create(self, user_id: int) -> RepeatSession:
        """Создать новую сессию"""
        ...

    async def get(self, session_id: int) -> RepeatSession | None:
        """Получить сессию по ID"""
        ...

    async def set_current_card(self, session_id: int, card_id: int) -> None:
        """Установить текущую карточку сессии"""
        ...

    async def complete_session(self, session_id: int) -> None:
        """Завершить сессию"""
        ...


class IRepeatSessionCardRepository(Protocol):
    async def create(self, session_id: int, card_id: int) -> RepeatSessionCard:
        """Создать запись карточки в сессии"""
        ...

    async def get(self, session_card_id: int) -> RepeatSessionCard | None:
        """Получить запись карточки в сессии по ID"""
        ...

    async def update(self, session_card: RepeatSessionCard) -> None:
        """Обновить запись карточки в сессии"""
        ...

    async def get_next_unfinished(self, session_id: int, after_id: int | None = None) -> RepeatSessionCard | None:
        """Получить следующую незавершенную карточку в сессии"""
        ...
