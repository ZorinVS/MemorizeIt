from datetime import datetime, timedelta
from app.domain.repositories import ICardRepetitionStateRepository
from app.domain.services.schedulers import RepetitionScheduler
from app.domain.models import CardRepetitionState


class RepeatCardUseCase:
    """Юзкейс для обработки повторения карточки с обновлением состояния."""

    def __init__(
        self,
        repetition_repo: ICardRepetitionStateRepository,
        scheduler: RepetitionScheduler,
    ):
        self.repetition_repo = repetition_repo
        self.scheduler = scheduler

    async def execute(self, card_id: int, score: int) -> CardRepetitionState:
        """Обрабатывает повторение карточки и обновляет состояние.

        Args:
            card_id: Идентификатор карточки.
            score: Оценка воспроизведения (0 — не вспомнил, 1 — с трудом, 2 — легко).

        Returns:
            Обновлённое состояние повторения карточки.
        """
        state = await self.repetition_repo.get_by_card_id(card_id)
        if state is None:
            raise ValueError(f"Repetition state for card_id={card_id} not found")

        interval, ef, n = self.scheduler.update(score, state.repetition, state.ef, state.interval)

        now = datetime.now(datetime.UTC)
        state.interval = interval
        state.ef = ef
        state.repetition = n
        state.last_reviewed_at = now
        state.next_review_at = now + timedelta(days=interval)

        await self.repetition_repo.update(state)

        return state
