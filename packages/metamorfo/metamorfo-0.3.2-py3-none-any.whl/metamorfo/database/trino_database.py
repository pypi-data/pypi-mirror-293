from os import getenv

from sqlalchemy import create_engine, text
from sqlalchemy.engine.cursor import CursorResult

from metamorfo.utility import hexa_b64


class TrinoDatabase:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        connection_key: str = hexa_b64(str(kwargs))
        if connection_key not in cls._instances:
            cls._instances[connection_key] = super(__class__, cls).__new__(cls)
        return cls._instances[connection_key]

    def __init__(self, *args, **kwargs) -> None:
        self._connection_key = (
            args[0] if len(args) > 0 else hexa_b64(str(kwargs))
        )

        if kwargs == {}:
            user: str = getenv("METAMORFO_TRINO_USER")
            pssw: str = getenv("METAMORFO_TRINO_PASSWORD")
            host: str = getenv("METAMORFO_TRINO_HOST")
            port: str = getenv("METAMORFO_TRINO_PORT")
            source: str = getenv("METAMORFO_TRINO_SOURCE")
        else:
            user: str = kwargs["username"]
            pssw: str = kwargs["password"]
            host: str = kwargs["host"]
            port: str = kwargs["port"]
            source: str = (
                kwargs["source"]
                if "source" in kwargs is not None
                else "default"
            )

        self.__engine(
            user=user, pssw=pssw, host=host, port=port, source=source
        )

    def __engine(
        self, user: str, pssw: str, host: str, port: str, source: str
    ) -> None:
        if pssw is not None:
            con_: str = f"trino://{user}:{pssw}@{host}:{port}?source={source}"
        else:
            con_: str = f"trino://{user}@{host}:{port}?source={source}"

        self.engine = create_engine(con_)

    def execute_query(self, query: str, params: dict = None) -> CursorResult:
        with self.engine.connect() as conn:
            if params is None:
                result = conn.execute(text(query))
            else:
                result = conn.execute(text(query), params)

            return result
