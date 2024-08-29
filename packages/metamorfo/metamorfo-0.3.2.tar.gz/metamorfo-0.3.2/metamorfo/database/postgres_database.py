from os import getenv
from metamorfo.utility import hexa_b64

from sqlalchemy import create_engine, text
from sqlalchemy.engine.cursor import CursorResult


class PostgresDatabase:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        connection_key = hexa_b64(str(kwargs))

        if connection_key not in cls._instances:
            cls._instances[connection_key] = super(__class__, cls).__new__(cls)
        return cls._instances[connection_key]

    def __init__(self, *args, **kwargs) -> None:
        self._connection_key: str = (
            args[0] if len(args) > 0 else hexa_b64(str(kwargs))
        )

        if kwargs == {}:
            user: str = getenv("METAMORFO_POSTGRES_USER")
            pssw: str = getenv("METAMORFO_POSTGRES_PASSWORD")
            host: str = getenv("METAMORFO_POSTGRES_HOST")
            port: str = getenv("METAMORFO_POSTGRES_PORT")
            database: str = getenv("METAMORFO_POSTGRES_DB")
        else:
            user: str = kwargs["username"]
            pssw: str = kwargs["password"]
            host: str = kwargs["host"]
            port: str = kwargs["port"]
            database: str = kwargs["database"]

        self.__connect(
            user=user, pssw=pssw, host=host, port=port, database=database
        )

    def __connect(
        self, user: str, pssw: str, host: str, port: str, database: str
    ) -> None:
        self.engine = create_engine(
            f"postgresql+psycopg2://{user}:{pssw}@{host}:{port}/{database}"
        )

    def execute_query(self, query: str, params: dict = None) -> CursorResult:
        with self.engine.connect() as conn:
            if params is None:
                result = conn.execute(text(query))
            else:
                result = conn.execute(text(query), params)

            return result
