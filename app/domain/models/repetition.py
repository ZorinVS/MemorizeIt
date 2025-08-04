from tortoise import fields
from app.domain.models.base import BaseModel


class CardRepetitionState(BaseModel):
    """Состояние повторения карточки."""

    card = fields.OneToOneField("models.Card", related_name="repetition_state", on_delete=fields.CASCADE)
    ef = fields.FloatField()
    interval = fields.IntField()
    repetition = fields.IntField()
    last_reviewed_at = fields.DatetimeField(null=True, default=None)
    next_review_at = fields.DatetimeField()

    class Meta:
        table = "repetitions"
        indexes = [("next_review_at",)]

    def __str__(self):
        return super().__str__().replace(
            "...",
            f"card={self.card}, next_review_at={self.next_review_at}"
        )

# class CardRepetitionState(Base):
#     """Состояние повторения для конкретной карточки.
#
#     Отражает текущие параметры алгоритма повторения SM-2.
#
#     Attributes:
#         id: Уникальный идентификатор записи.
#         card_id: Внешний ключ на карточку (уникальный, 1:1).
#         ef: Коэффициент лёгкости (Easiness Factor).
#         interval: Интервал до следующего повторения (в днях).
#         repetition: Количество успешных повторений подряд.
#         last_reviewed_at: Дата последнего повторения (если было).
#         next_review_at: Дата следующего рекомендованного повторения.
#         card: Обратная связь на карточку.
#
#     Notes:
#         В строковом представлении (__repr__) выводятся следующие поля:
#          - id
#          - card_id
#          - next_review_at
#     """
#     __tablename__ = "repetition_states"
#
#     card_id: Mapped[int] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"), unique=True, nullable=False)
#     ef: Mapped[float] = mapped_column(nullable=False)
#     interval: Mapped[int] = mapped_column(nullable=False)
#     repetition: Mapped[int] = mapped_column(nullable=False)
#     last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     next_review_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
#
#     card: Mapped["Card"] = relationship(
#         back_populates="repetition_state",
#         lazy="joined",
#     )
#
#     repr_cols_num: ClassVar[int] = 2
#     repr_cols: ClassVar[tuple[str]] = ("next_review_at",)
