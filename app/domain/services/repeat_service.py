from datetime import datetime, timedelta, timezone
from abc import ABC, abstractmethod
from app.domain.models import Card, CardRepetitionState
from app.domain.services.schedulers import RepetitionScheduler
from app.domain.repositories import ICardRepetitionStateRepository


class IRepeatCardService(ABC):
    @abstractmethod
    async def repeat(self, card: Card, score: int) -> None:
        """Обновить параметры повторения карточки по оценке пользователя."""
        pass


class RepeatCardService(IRepeatCardService):
    def __init__(
        self,
        scheduler: RepetitionScheduler,
        state_repo: ICardRepetitionStateRepository,
    ):
        self.scheduler = scheduler
        self.state_repo = state_repo

    async def repeat(self, card: Card, score: int) -> None:
        state = card.repetition_state if isinstance(card.repetition_state, CardRepetitionState) else None

        if state is None:
            interval, ef, n = self.scheduler.init()
        else:
            interval, ef, n = self.scheduler.update(
                score=score,
                n=state.repetitions,
                ef=state.easiness,
                interval=state.interval,
            )

        next_review_at = datetime.now(timezone.utc) + timedelta(days=interval)

        if state is None:
            state = CardRepetitionState(
                card_id=card.id,
                interval=interval,
                easiness=ef,
                repetitions=n,
                next_review_at=next_review_at,
            )
            await self.state_repo.create(state)
        else:
            state.interval = interval
            state.easiness = ef
            state.repetitions = n
            state.next_review_at = next_review_at
            await self.state_repo.update(state)
