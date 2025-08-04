from datetime import datetime, timezone

from app.domain.services.repeat_service import IRepeatCardService
from app.domain.repositories import IRepeatSessionRepository, ICardRepository, IRepeatSessionCardRepository
from app.domain.models import RepeatSession, RepeatSessionCard, Card


class RepeatSessionService:
    def __init__(
            self,
            session_repo: IRepeatSessionRepository,
            session_card_repo: IRepeatSessionCardRepository,
            card_repo: ICardRepository,
            repeat_card_service: IRepeatCardService,
    ):
        self.session_repo = session_repo
        self.session_card_repo = session_card_repo
        self.card_repo = card_repo
        self.repeat_service = repeat_card_service

    async def start_session(self, user_id: int) -> RepeatSession:
        active_session = await self.session_repo.get_active_session(user_id)
        if active_session:
            await self.session_repo.complete_session(active_session.id)

        # Получаем карточки для повторения
        now = datetime.now(timezone.utc)
        due_cards = await self.card_repo.get_due_cards_by_user(user_id, now)

        if not due_cards:
            raise NoCardsToRepeatError("No cards for repetition")

        # Создаем новую сессию
        session = await self.session_repo.create(user_id)

        # Добавляем карточки в сессию
        session_cards = []
        for card in due_cards:
            sc = await self.session_card_repo.create(session.id, card.id)
            session_cards.append(sc)

        # Устанавливаем первую карточку как текущую
        if session_cards:
            await self.session_repo.set_current_card(session.id, session_cards[0].id)

        return session

    async def get_current_card(self, session_id: int) -> tuple[Card, RepeatSessionCard]:
        session = await self.session_repo.get(session_id)
        if not session or not session.current_session_card_id:
            raise SessionNotFoundError("Session or current card not found")

        # Получаем текущую карточку сессии
        session_card = await self.session_card_repo.get(session.current_session_card_id)
        if not session_card:
            raise SessionNotFoundError("Session card not found")

        # Получаем основную карточку
        card = await self.card_repo.get_by_id(session_card.card_id)
        if not card:
            raise CardNotFoundError("Card not found")

        return card, session_card

    async def _move_to_next_card(self, session: RepeatSession) -> tuple[Card, RepeatSessionCard] | None:
        # Находим следующую незавершенную карточку
        next_sc = await self.session_card_repo.get_next_unfinished(
            session.id,
            after_id=session.current_session_card_id
        )

        # Если следующая карточка найдена
        if next_sc:
            await self.session_repo.set_current_card(session.id, next_sc.id)

            # Получаем основную карточку
            card = await self.card_repo.get_by_id(next_sc.card_id)
            if not card:
                raise CardNotFoundError("Card not found")

            return card, next_sc

        # Если карточек больше нет - завершаем сессию
        await self.session_repo.complete_session(session.id)
        return None

    async def process_answer(
            self,
            session_id: int,
            answer: str,
            is_idk: bool = False
    ) -> ProcessResult:
        session = await self.session_repo.get(session_id)
        if not session or not session.current_session_card_id:
            raise SessionNotFoundError("Session not found")

        # Получаем текущую карточку сессии и основную карточку
        card, session_card = await self.get_current_card(session_id)

        session_card.attempts += 1

        # Обработка "Не знаю"
        if is_idk:
            score = 0
            session_card.is_finished = True
            session_card.final_score = score
            await self.session_card_repo.update(session_card)
            await self.repeat_service.repeat(card, score)

            next_card_info = await self._move_to_next_card(session)
            return ProcessResult(skipped=True, correct=False, score=score, next_card=next_card_info)

        # Проверка ответа
        is_correct = answer.strip().lower() == card.answer.strip().lower()

        # Если ответ неверный - оставляем карточку текущей
        if not is_correct:
            await self.session_card_repo.update(session_card)
            return ProcessResult(correct=False, attempts=session_card.attempts)

        # Если ответ верный - обрабатываем
        score = 2 if session_card.attempts == 1 else 1
        session_card.is_finished = True
        session_card.final_score = score
        await self.session_card_repo.update(session_card)
        await self.repeat_service.repeat(card, score)

        next_card_info = await self._move_to_next_card(session)
        return ProcessResult(
            correct=True,
            score=score,
            next_card=next_card_info,
            session_completed=next_card_info is None
        )
