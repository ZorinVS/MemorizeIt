from typing import Protocol
from app.domain.models import CardRepetitionState


class ICardRepetitionStateRepository(Protocol):
    async def get_by_card_id(self, card_id: int) -> CardRepetitionState | None:
        """Получить состояние повторения по ID карточки."""
        ...

    async def create(self, state: CardRepetitionState) -> CardRepetitionState:
        """Создать новое состояние повторения."""
        ...

    async def update(self, state: CardRepetitionState) -> CardRepetitionState:
        """Обновить состояние повторения."""
        ...

    async def delete_by_card_id(self, card_id: int) -> None:
        """Удалить состояние повторения по ID карточки."""
        ...
