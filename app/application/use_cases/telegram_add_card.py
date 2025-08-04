from app.domain.repositories import IUserRepository, ICardRepository
from app.domain.models import Card
from app.interfaces.telegram.schemas import AddCardRequest


class TelegramAddCardUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        card_repo: ICardRepository,
    ):
        self.user_repo = user_repo
        self.card_repo = card_repo

    async def execute(self, data: AddCardRequest) -> Card:
        user = await self.user_repo.get_by_tg_id(data.tg_id)
        if not user:
            raise ValueError("User not found")

        card = await self.card_repo.create(Card(
            user=user,
            question=data.question,
            answer=data.answer,
        ))

        return card
