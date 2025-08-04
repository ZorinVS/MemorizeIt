from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "email" VARCHAR(255) UNIQUE,
    "password_hash" VARCHAR(255),
    "tg_id" BIGINT UNIQUE,
    "tg_first_name" VARCHAR(255),
    "tg_last_name" VARCHAR(255),
    "tg_username" VARCHAR(255),
    "is_active" BOOL NOT NULL DEFAULT True
);
COMMENT ON TABLE "users" IS 'Пользователь сервиса.';
CREATE TABLE IF NOT EXISTS "cards" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "question" TEXT NOT NULL,
    "answer" TEXT NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "cards" IS 'Карточка с вопросом и ответом.';
CREATE TABLE IF NOT EXISTS "repetitions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ef" DOUBLE PRECISION NOT NULL,
    "interval" INT NOT NULL,
    "repetition" INT NOT NULL,
    "last_reviewed_at" TIMESTAMPTZ,
    "next_review_at" TIMESTAMPTZ NOT NULL,
    "card_id" INT NOT NULL UNIQUE REFERENCES "cards" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "repetitions" IS 'Состояние повторения карточки.';
CREATE TABLE IF NOT EXISTS "repeat_session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "started_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "finished_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "repeat_session" IS 'Сессия повторения карточек пользователем.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
