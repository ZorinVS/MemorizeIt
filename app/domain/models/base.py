from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    """Абстрактная база для всех моделей."""
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, ...)"
