from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "avatar_url" VARCHAR(255) NOT NULL DEFAULT 'https://example.com/default-avatar.png',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "user" IS 'Пользователи ';
CREATE TABLE IF NOT EXISTS "notification" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(7) NOT NULL,
    "text" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "notification"."type" IS 'like: like\ncomment: comment\nrepost: repost';
COMMENT ON TABLE "notification" IS 'Уведомления ';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmFtP2zAUx79KlCcmbVBCOyreCpSNbbQTdBdtTJGbnLYWiZ3ZzqCa+t1nO3Fz74pUWJ"
    "l4Mem5OPbPJ/Yf/7ZD6kPAdwdU4An2kMCU2EfWb5ugEORDrf+lZaMoyrzKINA40AmkHDnm"
    "giFPSN8EBRykyQfuMRyl77Kv41bbOVDtgaPbjm7bugXderod57y+bruqbU8s9SKfevJNmE"
    "w32GdM8M8YXEGnIGbAZM/ff0gzJj7cATc/oxt3giHwC+CwrzrQdlfMI207J+JMB6rhjl2P"
    "BnFIsuBoLmaULKMxEco6BQIMCVDdCxYrgCQOgpS3YZqMNAtJhpjL8WGC4kAtg8qurIIx5i"
    "CmJo8StYJyNFxPcKre8srZbx+2uwev210ZokeytBwukullc08SNYHByF5oPxIoidAYM256"
    "9hVyJzPE+iQONb5zOSBEPKhgNLklkHL4ZZAG2yqSxpChzAp4JUs7wDdwZKn2mng0DIGIIy"
    "t9uCYMIsqlIflbLt0G6iG6cwMgUzGTP1cR/ty7PHnbu9w5fKF6pvLTS77LQepwlEctQQ45"
    "3Ikq8pG01lerif/HmNcu2RW0Rv2vIzXokPOfQR7TzkXvqyYYzlPPh+HgjQnPYT35MDwu8f"
    "QYqPm7qIbqqfQIHEI92WJmia+fpu6ah+2kbcs5+EMSzNO9ZxX984v+1ah38bGwBKe9UV95"
    "nAJ+Y915XSrsZSfWl/PRW0v9tL4NB31NUH5gU6bfmMWNvtlqTCgW1CX01kV+bps0VgOmsL"
    "AxB+Zi373X3l5M+vsevyWruIFtXp2Nk5vaXT6FUsV4RhngKXkP88pWX0KXKpNPsqftRLgw"
    "lWCsWZUxdLuUDKUCkTOU8wKRHHu9q5Pead/WKMfIu7lFzHcLTJWHOrRkWcZWXaETli2IoK"
    "lGoCaihp1nW6MGDfNmFRibiLXU3/4kp8u0Imsn6uwwZ090XEt785ouUXDdeg24sZ6fleCj"
    "K0FVQ/q5Vg02b7YmZzPy5MEpFpRdp7WGtOu0GrWdchXFSIQ4v6VyJ5ghPrsPykriU5F7Ra"
    "L7TncNpDKqkan2FaGiX7JomRuz4D5Ei1mPh9OeCRHxo709uENhFMCu/FdkL3W/Sga1G0mg"
    "m0LudDprIJdRjci171lU/7eiuqIMm/VNVgH5myVeLYLjNP3s/SUEy+unetFYvs7avgVvEo"
    "+Lh9R7PWDYm9UpvtSzUvOhLOZvqq8Zw7POenSd9QsYT7+DdU+yXMrTVAUPckSpT+M+ciAJ"
    "f5oA91vrKFUZ1SyrWhWtKt8ogNQc8O+uhoOGwz1LKYH8ROQEv/vYEy+tAHPxYzuxrqCoZr"
    "36crJ8D1k6nVUHx3UXMY95nbD4A584bZk="
)
