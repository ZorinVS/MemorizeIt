from app.domain.models import User
from app.domain.repositories import IUserRepository


class UserRepository(IUserRepository):
    async def get_by_email(self, email: str) -> User | None:
        return await User.filter(email=email).first()

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        return await User.filter(tg_id=tg_id).first()

    async def get_by_id(self, user_id: int) -> User | None:
        return await User.filter(id=user_id).first()

    async def add(self, user: User) -> User:
        await user.save()
        return user

    async def list_active_users(self) -> list[User]:
        return await User.filter(is_active=True).all()
