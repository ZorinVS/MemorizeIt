from datetime import datetime, timezone
from app.domain.repositories import IRepeatSessionRepository, IRepeatSessionCardRepository


class StartRepeatSessionUseCase:
    """Запускает сессию повторения карточек пользователя."""

    def __init__(
            self,
            card_session_repo: IRepeatSessionCardRepository,
            session_repo: IRepeatSessionRepository,
    ):
        self.card_session_repo = card_session_repo
        self.session_repo = session_repo

    async def execute(self, user_id: int, card_ids: list[int]) -> None:
        session = await self.session_repo.get_by_user(user_id)

        if session:
            # Сброс старой сессии
            await self.card_session_repo.delete_by_session(session.id)
            await self.session_repo.reset(session)
        else:
            # Создание новой
            session = await self.session_repo.create(user_id)

        # Добавляем карточки в сессию
        for card_id in card_ids:
            await self.card_session_repo.add(session.id, card_id)

