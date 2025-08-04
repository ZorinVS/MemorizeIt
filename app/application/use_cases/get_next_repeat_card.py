# from app.domain.repositories import ICardRepository, IUserRepository, IRepeatSessionRepository
# from app.domain.services.sessions.repeat_session_manager import RepeatSessionManager
# from app.domain.models import Card
#
#
# class GetNextRepeatCardUseCase:
#     """Выдаёт следующую карточку для повторения."""
#
#     def __init__(
#         self,
#         user_repo: IUserRepository,
#         card_repo: ICardRepository,
#         session_repo: IRepeatSessionRepository,
#         session_manager: RepeatSessionManager,
#     ):
#         self.user_repo = user_repo
#         self.card_repo = card_repo
#         self.session_repo = session_repo
#         self.session_manager = session_manager
#
#     async def execute(self, tg_id: int) -> Card | None:
#         user = await self.user_repo.get_by_tg_id(tg_id)
#         if not user:
#             return None
#
#         session = await self.session_repo.get_active_by_user(user.id)
#         if not session:
#             return None
#
#         card_id = self.session_manager.get_next_card(user.id)
#         if card_id is None:
#             return None
#
#         card = await self.card_repo.get_by_id(card_id)
#         return card
