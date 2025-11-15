from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notifications" DROP CONSTRAINT IF EXISTS "fk_notifica_users_f7be8ea3";
        ALTER TABLE "notifications" RENAME COLUMN "user_id_id" TO "user_id";
        ALTER TABLE "notifications" ADD CONSTRAINT "fk_notifica_users_ca29871f" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notifications" DROP CONSTRAINT IF EXISTS "fk_notifica_users_ca29871f";
        ALTER TABLE "notifications" RENAME COLUMN "user_id" TO "user_id_id";
        ALTER TABLE "notifications" ADD CONSTRAINT "fk_notifica_users_f7be8ea3" FOREIGN KEY ("user_id_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "eJztmO1P4jAcx/+VZa+8RBEmHIR3E/HkVLjovDM+ZClb2Ra2bm6dQAz/+7Xdxp4nJMjhxT"
    "d1/B66/j7t2q994y1bhaZXG9rYmBgKwIaN+C73xiNgQfJQ6D/keOA4sZcaMBibLAElIpkH"
    "jD3sAgUT5wSYHiQmFXqKazjhy/gnv94UTmh7IrC2xdomayFrFdaOE16VtR3aNiccfZFqK+"
    "RNBtK22KePjBcfytjWINahS3p+fCZmA6lwDr3opzOVJwY01RQ5Q6UdMLuMFw6zDRA+Z4F0"
    "uGNZsU3fQnGws8C6jVbRBsLUqkEEXYAh7R67PgWIfNMMgUdMg5HGIcEQEzkqnADfpNNAs3"
    "OzEBkTEEOTQiaSzCAZjccK1OhbjoRGs93snHxvdkgIG8nK0l4G5cW1B4mMwFDil8wPMAgi"
    "GMaYG6s+R66nA7ePfIvhG5ABAaTAHMYoNwOSDD8LMsJWRTIyxCjjBVzJkjeNKexytH1Cim"
    "1ZEOEuFz48IRc6tkcMwd/s0i2hboG5bEKkYZ38rCL8W7zpXYg3B+1vtGebfHrBhzkMHQL1"
    "0ClIIIdznEcuEWvxao3i/zHmtZdsBS2pfy/RQVue92ImMR1ci/eMoLUIPVej4Y8oPIG1dz"
    "U6zfBUXEjrl0EB1TPiwYYFi8mmMzN81TC1Fj3sJ22e1KCOkLkI954q+oPr/q0kXv9KTcGZ"
    "KPWpR0jhj6wH3zMLe9UJ92cgXXD0J/cwGvYZQfKBaS57YxwnPfB0TMDHtozsmQzUxDYZWS"
    "MwqYn1PejKG23siYz3d/c9mb8tbPD0VJxMC/d3SiQP8Nx2oaGhS7jI7fAZbqEiuQu72T9+"
    "y2gNRNZ4cblgtlIKyaVByiNFQRwcdeJtTzzr8wziGCjTGXBVOUWTemzBzlhWsXmXJVhZC0"
    "BAY/XTKuiYk2ALJGAEvFz60YI2kHyNSUKMMRnWDCRZO2EPxFudeZNCLpBtnWLht7Wev+Tf"
    "zuUfXUTsuVAClm+yUc52NMmHU0zJuVZ9DT3XqpcKOupKKxAHeN7MJluBDjx9E5S5xM+i8d"
    "JEG0JnDaQkqpQp86WhgleyaF3Zd81NiKazdoeT1zF2vO7xMZwDyzFhjfz/cRy6j4JB1RwC"
    "dFvIhVZrDeQkqhQ5830p6f9WSedEYbnAiVdA7j4pvQhOw/Tzyxtorq6niiVj9hJr/ya8TD"
    "ouP1LwidA1FL1I8oWeStEH4pj3VF85hi+dtXOd9Uq0evgdrHuSJVI+pyr4kCOKfhqbyIEg"
    "/HMCbNTXUaokqlxW1XNalbwRQ1RwwP+8HQ1LDvc4JQPyDpECH1VDwYecaXj4eT+xVlCkVV"
    "ffSGYvHzOnM+3gtOgOZpf3Ccu/Yptpzw=="
)
