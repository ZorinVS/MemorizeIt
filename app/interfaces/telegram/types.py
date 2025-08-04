from typing import Annotated
from fastapi import Body

from app.interfaces.telegram.schemas import StartRequest, AddCardRequest, DoRepeatRequest, RepeatAnswerRequest

StartBody = Annotated[StartRequest, Body()]
AddCardBody = Annotated[AddCardRequest, Body()]
DoRepeatBody = Annotated[DoRepeatRequest, Body()]
RepeatAnswerBody = Annotated[RepeatAnswerRequest, Body()]
