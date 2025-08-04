from tortoise import fields
from app.domain.models.base import BaseModel


class RepeatSession(BaseModel):
    """Сессия повторения карточек пользователем."""
    user = fields.OneToOneField("models.User", related_name="repeat_session", on_delete=fields.CASCADE)
    is_active = fields.BooleanField(default=True)
    started_at = fields.DatetimeField(auto_now_add=True)
    finished_at = fields.DatetimeField(null=True)
    session_cards: fields.ReverseRelation["RepeatSessionCard"]
    current_session_card = fields.IntField(null=True)

    class Meta:
        table = "repeat_session"


class RepeatSessionCard(BaseModel):
    """Состояние повторения карточки."""
    session = fields.ForeignKeyField("models.RepeatSession", related_name="cards", on_delete=fields.CASCADE)
    card = fields.ForeignKeyField("models.Card", related_name="in_sessions", on_delete=fields.CASCADE)
    attempts = fields.IntField(default=0)
    is_finished = fields.BooleanField(default=False)
    final_score = fields.IntField(null=True)

    class Meta:
        table = "card_repeat_state"
