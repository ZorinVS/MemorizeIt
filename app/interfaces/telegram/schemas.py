from datetime import datetime

from pydantic import BaseModel, Field


class StartRequest(BaseModel):
    tg_id: int = Field(..., example=123456789)
    first_name: str | None = Field(None, example="John")
    username: str | None = Field(None, example="johndoe")
    last_name: str | None = Field(None, example="Doe")


class AddCardRequest(BaseModel):
    tg_id: int = Field(..., example=123456789)
    question: str = Field(..., example="constancy")
    answer: str = Field(..., example="постоянство")


class DoRepeatRequest(BaseModel):
    tg_id: int = Field(..., example=123456789)


class RepeatAnswerRequest(BaseModel):
    tg_id: int = Field(..., example=123456789)
    session_id: int = Field(..., example=1)
    answer: str = Field(..., example="постоянство")


class SkipCardRequest(BaseModel):
    tg_id: int = Field(..., example=123456789)
    session_id: int = Field(..., example=1)


# Response schemas
class StartResponse(BaseModel):
    user_id: int
    message: str


class AddCardResponse(BaseModel):
    card_id: int
    question: str
    answer: str
    created_at: datetime


class RepeatSessionResponse(BaseModel):
    session_id: int
    card_id: int
    question: str


class RepeatResultResponse(BaseModel):
    correct: bool
    attempts: int
    score: int | None = None
    next_question: str | None = None
    session_completed: bool = False


class SkipResultResponse(BaseModel):
    score: int = 0
    next_question: str | None = None
    session_completed: bool = False
