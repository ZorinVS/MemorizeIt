from datetime import datetime, timezone
from app.domain.models import RepeatSession, RepeatSessionCard
from app.domain.repositories import IRepeatSessionRepository, IRepeatSessionCardRepository


class RepeatSessionRepository(IRepeatSessionRepository):
    async def get_active_session(self, user_id: int) -> RepeatSession | None:
        return await RepeatSession.filter(
            user_id=user_id,
            is_active=True
        ).first()

    async def create(self, user_id: int) -> RepeatSession:
        return await RepeatSession.create(user_id=user_id)

    async def get(self, session_id: int) -> RepeatSession | None:
        return await RepeatSession.get_or_none(id=session_id)

    async def set_current_card(self, session_id: int, card_id: int) -> None:
        await RepeatSession.filter(id=session_id).update(current_session_card_id=card_id)

    async def complete_session(self, session_id: int) -> None:
        await RepeatSession.filter(id=session_id).update(
            is_active=False,
            finished_at=datetime.now(timezone.utc),
            current_session_card_id=None
        )


class RepeatSessionCardRepository(IRepeatSessionCardRepository):
    async def create(self, session_id: int, card_id: int) -> RepeatSessionCard:
        return await RepeatSessionCard.create(
            session_id=session_id,
            card_id=card_id
        )

    async def get(self, session_card_id: int) -> RepeatSessionCard | None:
        return await RepeatSessionCard.get_or_none(id=session_card_id)

    async def update(self, session_card: RepeatSessionCard) -> None:
        await session_card.save()

    async def get_next_unfinished(self, session_id: int, after_id: int | None = None) -> RepeatSessionCard | None:
        query = RepeatSessionCard.filter(
            session_id=session_id,
            is_finished=False
        ).order_by("id")

        if after_id:
            query = query.filter(id__gt=after_id)

        return await query.first()
