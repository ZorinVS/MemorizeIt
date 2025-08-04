from app.domain.repositories import IUserRepository
from app.domain.models import User
from app.interfaces.telegram.schemas import StartRequest


class TelegramStartUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, data: StartRequest) -> User:
        user = await self.user_repo.get_by_tg_id(data.tg_id)
        if user:
            return user

        new_user = User(
            tg_id=data.tg_id,
            tg_first_name=data.first_name,
            tg_last_name=data.last_name,
            tg_username=data.username,
        )
        return await self.user_repo.add(new_user)
