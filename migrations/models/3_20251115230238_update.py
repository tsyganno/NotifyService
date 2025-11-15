from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME COLUMN "password_hash" TO "password";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME COLUMN "password" TO "password_hash";"""


MODELS_STATE = (
    "eJztmO1P4jAcx/+VZa+8RBEmHIR3E/HkVLjovDM+ZClbgYWtm10nEMP/fm23secJCXJ48U"
    "0dv4euv0+79mvfRMvWoelW+jYxRoYGiGEjsS28iQhYkD7k+g8FEThO5GUGAoYmT0CxSO4B"
    "Q5dgoBHqHAHThdSkQ1fDhhO8THzyqnXphLUnEm8bvK3zFvJW4+0w5tV522JtfSSwF+m2Rt"
    "9koPEW+/SQ8eJBldhjSCYQ054fn6nZQDqcQzf86UzVkQFNPUHO0FkH3K6ShcNtPUTOeSAb"
    "7lDVbNOzUBTsLMjERqtoAxFmHUMEMSCQdU+wxwAizzQD4CFTf6RRiD/EWI4OR8Az2TSw7M"
    "wshMYYxMCk0YmkM0hH4/ICx+wtR1Kt3qy3Tr7XWzSEj2RlaS798qLa/UROoK+IS+4HBPgR"
    "HGPEjVefIdeZANxFnsXx9eiAANJgBmOYmwJJh58GGWIrIxkaIpTRAi5lKZrGFLYF1j4hzb"
    "YsiEhbCB6eEIaO7VKD/ze9dAuoW2CumhCNyYT+LCP8W77pXMg3B81vrGebfnr+h9kPHBLz"
    "sCmIIYdzkkWuUGv+ag3j/zHmtZdsCS2le6+wQVuu+2LGMR1cy/ecoLUIPFeD/o8wPIa1cz"
    "U4TfHUMGT1qyCH6hn1EMOC+WSTmSm+epBaCR/2k7ZIa9AHyFwEe08Z/d5191aRr38lpuBM"
    "VrrMIyXwh9aD76mFvepE+NNTLgT2U3gY9LucIP3Axpi/MYpTHkQ2JuARW0X2TAV6bJsMrS"
    "GYxMR6LsTqRht7LOP93X1P5m8LGzw7FUfT3P2dEckCPLcxNMboEi4yO3yKW6BI7oJu9o/f"
    "MlwDoTVaXBjMVkohvjRoebQoSPyjTr7tyGddkUMcAm06A1hXEzSZx5bslGUVm3VZkpW2AA"
    "TGvH5WBRtzHGyOBAyBF0s/VtAGkq82iokxLsPqviRrxuy+eKtyb1zI+bKtlS/8ttbzl/zb"
    "ufxji4g/50rA4k02zNmOJvlwigk516iuoeca1UJBx1xJBeIA153ZOGcNFlOM53wWZZfkWJ"
    "Naa4CkUYUkuS+JErzSpYpVD5ubwExm7Q6nOCHEcdvHx3AOLMeEFfpfx3HgPvIHVXEo0G0h"
    "lxqNNZDTqELk3Peln/9b/ZyRgsWyJloBmVuk5CI4DdLPL2+gubqUyheK6aur/ZvwIsG4/E"
    "iZJ0NsaJM8oRd4SqUeiGLe03rFGL7U1c7V1StV6MF3sO5JFkv5nKrgQ44o9mlsIgf88M8J"
    "sFZdR5/SqGJZVc0oVPpGAlHOAf/zdtAvONyjlBTIO0QLfNQNjRwKpuGS5/3EWkKRVV1+D5"
    "m+ckydzqyD07ybl13eIiz/Ak8pZck="
)
