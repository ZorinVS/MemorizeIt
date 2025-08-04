from datetime import datetime
from typing import Protocol
from app.domain.models import Card


class ICardRepository(Protocol):
    async def get_by_id(self, card_id: int) -> Card | None:
        """Получить карточку по ID."""
        ...

    async def list_by_user(self, user_id: int, only_active: bool = False) -> list[Card]:
        """Получить все карточки пользователя, опционально только активные."""
        ...

    async def create(self, card: Card) -> Card:
        """Создать новую карточку."""
        ...

    async def delete(self, card_id: int) -> None:
        """Удалить карточку по ID."""
        ...

    async def get_due_cards(self, now: datetime) -> list[Card]:
        """Получить все карточки, которые необходимо повторить (next_review_at <= now).

        Только активные карточки, у которых есть состояние повторения.
        Обязательно должна быть загружена связь `card.user`.
        """
        ...

    async def get_due_cards_by_user(self, user_id: int, now: datetime) -> list[Card]:
        """Получить карточки пользователя, которые необходимо повторить (next_review_at <= now).

        Только активные карточки, у которых есть состояние повторения.
        Обязательно должна быть загружена связь `card.user`.
        """
        ...
