from app.domain.models import CardRepetitionState
from app.domain.repositories import ICardRepetitionStateRepository


class CardRepetitionStateRepository(ICardRepetitionStateRepository):
    async def get_by_card_id(self, card_id: int) -> CardRepetitionState | None:
        return await CardRepetitionState.get_or_none(card_id=card_id)

    async def create(self, state: CardRepetitionState) -> CardRepetitionState:
        await state.save()
        return state

    async def update(self, state: CardRepetitionState) -> CardRepetitionState:
        await state.save()
        return state

    async def delete_by_card_id(self, card_id: int) -> None:
        await CardRepetitionState.filter(card_id=card_id).delete()
