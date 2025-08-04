from tortoise import fields
from app.domain.models.base import BaseModel


class User(BaseModel):
    """Пользователь сервиса."""
    email = fields.CharField(max_length=255, null=True, unique=True)
    password_hash = fields.CharField(max_length=255, null=True)
    tg_id = fields.BigIntField(null=True, unique=True)
    tg_first_name = fields.CharField(max_length=255, null=True)
    tg_last_name = fields.CharField(max_length=255, null=True)
    tg_username = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)

    cards: fields.ReverseRelation["Card"]
    repeat_sessions: fields.ReverseRelation["RepeatSession"]

    class Meta:
        table = "users"

    def __str__(self):
        identity = f"email={self.email}" if self.email else f"tg_id={self.tg_id}"
        return super().__str__().replace("...", __new=identity)


# class User(Base):
#     """Пользователь сервиса.
#
#     Используется для авторизации через email или Telegram, а также для привязки карточек.
#
#     Attributes:
#         id: Уникальный идентификатор пользователя.
#         email: Email-адрес (если используется авторизация по email).
#         password_hash: Хеш пароля (если используется авторизация по email).
#         tg_id: Идентификатор Telegram-пользователя.
#         is_active: Флаг активности пользователя.
#         created_at: Дата и время регистрации.
#         cards: Список карточек, принадлежащих пользователю.
#     """
#     __tablename__ = "users"
#
#     email: Mapped[str | None] = mapped_column(unique=True, nullable=True)
#     password_hash: Mapped[str | None] = mapped_column(nullable=True)
#     tg_id: Mapped[int | None] = mapped_column(unique=True, nullable=True)
#     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
#     created_at: Mapped[CreatedAt]
#
#     cards: Mapped[list["Card"]] = relationship(
#         back_populates="User",
#         cascade="all, delete-orphan",
#         lazy="selectin",
#     )
#
#     def __repr__(self):
#         """Отображает id и email или tg_id (если email отсутствует)."""
#         identity = f"email={self.email}" if self.email else f"tg_id={self.tg_id}"
#         return f"<{self.__class__.__name__} id={self.id} {identity}>"
