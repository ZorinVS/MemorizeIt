from tortoise import fields
from app.domain.models.base import BaseModel


class Card(BaseModel):
    """Карточка с вопросом и ответом."""

    user = fields.ForeignKeyField("models.User", related_name="cards", on_delete=fields.CASCADE)
    question = fields.TextField()
    answer = fields.TextField()
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)

    repetition_state: fields.ReverseRelation["CardRepetitionState"]
    in_sessions: fields.ReverseRelation["RepeatSessionCard"]

    class Meta:
        table = "cards"

    def __str__(self):
        return super().__str__().replace(
            "...",
            f"user={self.user}, question={self.question}"
        )


# class Card(Base):
#     """Карточка с вопросом и ответом, создаваемая пользователем.
#
#     Используется в системе интервального повторения.
#
#     Attributes:
#         id: Уникальный идентификатор карточки.
#         user_id: Внешний ключ на пользователя-владельца.
#         question: Вопрос или термин.
#         answer: Ответ или перевод.
#         is_active: Флаг, указывающий, участвует ли карточка в повторении.
#         created_at: Дата создания карточки.
#         updated_at: Дата последнего обновления (если было).
#         user: Пользователь-владелец карточки.
#         repetition_state: Состояние повторения карточки (1:1).
#     """
#     __tablename__ = "cards"
#
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     question: Mapped[str] = mapped_column(nullable=False)
#     answer: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
#     created_at: Mapped[CreatedAt]
#     updated_at: Mapped[UpdatedAt]
#
#     user: Mapped["User"] = relationship(
#         back_populates="cards",
#         lazy="joined",
#     )
#
#     repetition_state: Mapped["CardRepetitionState"] = relationship(
#         back_populates="card",
#         uselist=False,
#         cascade="all, delete-orphan",
#         lazy="joined",
#     )
