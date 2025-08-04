from app.domain.repositories import ICardRepository, ICardRepetitionStateRepository
from app.domain.models import Card, CardRepetitionState
from app.domain.services.schedulers import RepetitionScheduler
from datetime import datetime, timedelta


class CreateCardUseCase:
    """Создаёт новую карточку и инициализирует её параметры повторения."""

    def __init__(
        self,
        card_repo: ICardRepository,
        repetition_repo: ICardRepetitionStateRepository,
        scheduler: RepetitionScheduler,
    ):
        self.card_repo = card_repo
        self.repetition_repo = repetition_repo
        self.scheduler = scheduler

    async def execute(self, user_id: int, question: str, answer: str) -> Card:
        """Создаёт карточку и соответствующее состояние повторения.

        Args:
            user_id: Идентификатор пользователя.
            question: Вопрос карточки.
            answer: Ответ карточки.

        Returns:
            Объект созданной карточки.
        """
        card = Card(user_id=user_id, question=question, answer=answer)
        card = await self.card_repo.create(card)

        interval, ef, n = self.scheduler.init()
        repetition_state = CardRepetitionState(
            card_id=card.id,
            ef=ef,
            interval=interval,
            repetition=n,
            next_review_at=datetime.now(datetime.UTC) + timedelta(days=interval),
        )
        await self.repetition_repo.create(repetition_state)

        return card
