from datetime import datetime

from app.domain.models import Card
from app.domain.repositories import ICardRepository


class CardRepository(ICardRepository):
    async def get_by_id(self, card_id: int) -> Card | None:
        return (
            await Card.filter(id=card_id)
            .prefetch_related("user", "repetition_state")
            .first()
        )

    async def list_by_user(self, user_id: int, only_active: bool = False) -> list[Card]:
        query = Card.filter(user_id=user_id)
        if only_active:
            query = query.filter(is_active=True)
        return await query.prefetch_related("repetition_state").all()

    async def create(self, card: Card) -> Card:
        await card.save()
        return card

    async def delete(self, card_id: int) -> None:
        await Card.filter(id=card_id).delete()

    async def get_due_cards(self, now: datetime) -> list[Card]:
        """
        Получить все активные карточки, которые необходимо повторить (next_review_at <= now).

        Загружает связи: card.repetition_state и card.user
        """
        return await Card.filter(
            is_active=True,
            repetition_state__next_review_at__lte=now,
        ).prefetch_related(
            "user",
            "repetition_state",
        ).all()

    async def get_due_cards_by_user(self, user_id: int, now: datetime) -> list[Card]:
        return await Card.filter(
            user_id=user_id,
            is_active=True,
            repetition_state__next_review_at__lte=now,
        ).prefetch_related(
            "user",
            "repetition_state",
        ).all()
