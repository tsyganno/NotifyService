from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notification" RENAME TO "notifications";
        ALTER TABLE "user" RENAME TO "users";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME TO "user";
        ALTER TABLE "notifications" RENAME TO "notification";"""


MODELS_STATE = (
    "eJztmO1P4jAcx/+VZa+8RBEmHIR3iHhyKlx03hkfspStbA1bN7dOIIb//dpuY88ICXJ48U"
    "0dv4euv0+79mvfRMvWoOlVBjZBY6QCgmwstoU3EQML0odC/6EgAseJvcxAwMjkCTgRyT1g"
    "5BEXqIQ6x8D0IDVp0FNd5IQvE5/8al06Ye2JxNsGb+u8hbxVeTtKeDXetlhbHwvsRZqt0j"
    "chrG+xTx+jFx8qxNYhMaBLe358pmaENTiDXvTTmShjBE0tRQ5prANuV8jc4bY+Juc8kA13"
    "pKi26Vs4DnbmxLDxMhphwqw6xNAFBLLuieszgNg3zRB4xDQYaRwSDDGRo8Ex8E02DSw7Nw"
    "uRMQExNKl0IukM0tF4vECdveVIqtWb9dbJ93qLhvCRLC3NRVBeXHuQyAkMZHHB/YCAIIJj"
    "jLnx6nPkugZwe9i3OL4+HRDAKsxhjHIzIOnwsyAjbKtIRoYYZbyAV7IUTTSBbYG1T1i1LQ"
    "ti0hbChyfsQsf2qCH4m126JdQtMFNMiHVi0J+rCP/u3HQvOjcHzW+sZ5t+esGHOQgdEvOw"
    "KUgghzOSRy5Ta/FqjeL/Mea1l+wKWnLvXmaDtjzvxUxiOrju3HOC1jz0XA0HP6LwBNbu1f"
    "A0w1N1IatfAQVUz6iHIAsWk01nZvhqYWolethP2iKtQRticx7uPavo9697t3Ln+ldqCs46"
    "co95pBT+yHrwPbOwl50If/ryhcB+Cg/DQY8TpB+Y7vI3xnHyg8jGBHxiK9ieKkBLbJORNQ"
    "KTmljfg66CNGWjvT2d9P4evyezuIVtnp2N40nhLh9CyWM8t12IdHwJ57mtPoMulCZ3tKf9"
    "RLiIVkJkjVeZC6ZLyZBZILRCWhckwbHXue12znoiRzkC6mQKXE1JMWUeW7IzlmVs3mVJVt"
    "YCMNA5AlYIG3aSbYEcjJiXy0BW0wbyrzZOCDMuyeqBPGsm7IGQq3JvUtQFEq5VLAK31vOX"
    "FNy5FGSLiD8XysHy3TbK2Y4++XCKKWnXqK6h7RrVUnHHXGk14gDPm9p0KzCAZ2yCMpf4Wf"
    "RemmhNaq2BlEaVMuW+NFTwShetq/iuuQnRdNbucIoGIY7XPj6GM2A5JqzQ/0WOQ/dRMKiK"
    "Q4FuC7nUaKyBnEaVIue+L1X936rqnDQsFzjxCsjdLaUXwWmYfn55A83lVVWxasxeaO3fhJ"
    "epx8VHCr4OdJFqFEm+0LNS9IE45j3VV47hS2ftXGe9Uq0efgfrnmSJlM+pCj7kiGKfxiZy"
    "IAj/nABr1XWUKo0ql1XVnFalbyQQFxzwP2+Hg5LDPU7JgLzDtMBHDankUDCRR573E+sKiq"
    "zq1beT2YvIzOnMOjgtuonZ5X3C4i/1u25/"
)
