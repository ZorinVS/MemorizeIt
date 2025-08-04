from typing import Protocol
from app.domain.models import User


class IUserRepository(Protocol):
    async def get_by_email(self, email: str) -> User | None:
        """Получить пользователя по email (если используется авторизация по почте)."""
        ...

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        """Получить пользователя по Telegram ID (если используется Telegram-авторизация)."""
        ...

    async def get_by_id(self, user_id: int) -> User | None:
        """Получить пользователя по его ID."""
        ...

    async def add(self, user: User) -> User:
        """Сохранить нового пользователя в базу данных."""
        ...
