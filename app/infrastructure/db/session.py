# from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker as sessionmaker
#
# from app.infrastructure.db.config import settings
#
#
# engine: AsyncEngine = create_async_engine(url=settings.async_url, echo=True)
# async_sessionmaker = sessionmaker(bind=engine, expire_on_commit=False)
#
#
# async def get_async_session() -> AsyncSession:
#     async with async_sessionmaker() as session:
#         yield session
#
#
# if __name__ == '__main__':
#     print(type(async_sessionmaker))
