# from app.domain.repositories import ICardRepository
# from app.domain.services.sessions.repeat_session_manager import RepeatSessionManager
# from app.domain.services.schedulers import IRepeatCardService RepetitionScheduler
# from app.application.dto import SubmitRepeatAnswerResult  # или внутри этого файла
#
#
# class SubmitRepeatAnswerUseCase:
#     def __init__(
#         self,
#         card_repo: ICardRepository,
#         session_manager: RepeatSessionManager,
#         repeat_card_service: IRepeatCardService,
#     ):
#         self.card_repo = card_repo
#         self.session_manager = session_manager
#         self.repeat_card_service = repeat_card_service
#
#     async def execute(self, user_id: int, card_id: int, user_answer: str) -> SubmitRepeatAnswerResult:
#         card = await self.card_repo.get_by_id(card_id)
#         if card is None or card.user_id != user_id:
#             raise ValueError("Карточка не найдена или не принадлежит пользователю.")
#
#         correct_answer = card.word_translation
#         is_correct, is_finished = self.session_manager.submit_answer(
#             user_id=user_id,
#             card_id=card_id,
#             answer=user_answer,
#             correct_answer=correct_answer,
#         )
#
#         if is_finished:
#             session = self.session_manager.user_sessions[user_id][card_id]
#             score = session.final_score
#             await self.repeat_card_service.repeat(card, score)
#
#         return SubmitRepeatAnswerResult(
#             is_correct=is_correct,
#             is_finished=is_finished,
#             correct_answer=correct_answer,
#         )
