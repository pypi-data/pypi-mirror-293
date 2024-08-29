from os import getenv
from pymongo import MongoClient
from pymongo.collection import Collection
from metamorfo.utility import hexa_b64


class MongoDatabase:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        _connection_key: str = hexa_b64(str(kwargs))

        if _connection_key not in cls._instances:
            cls._instances[_connection_key] = super(__class__, cls).__new__(
                cls
            )
        return cls._instances[_connection_key]

    def __init__(self, *args, **kwargs) -> None:
        self._connection_key = (
            args[0] if len(args) > 0 else hexa_b64(str(kwargs))
        )
        if kwargs == {}:
            user: str = getenv("METAMORFO_MONGO_USER")
            pssw: str = getenv("METAMORFO_MONGO_PASSWORD")
            host: str = getenv("METAMORFO_MONGO_HOST")
            port: str = getenv("METAMORFO_MONGO_PORT")
        else:
            user: str = kwargs["username"]
            pssw: str = kwargs["password"]
            host: str = kwargs["host"]
            port: str = kwargs["port"]

        self.__connect(
            mongo_user=user, mongo_pssw=pssw, mongo_host=host, mongo_port=port
        )

    def __connect(
        self,
        mongo_user: str,
        mongo_pssw: str,
        mongo_host: str,
        mongo_port: str,
    ) -> None:
        self._mongo_client = MongoClient(
            f"mongodb://{mongo_user}:{mongo_pssw}@{mongo_host}:{mongo_port}/admin"
        )

    def list_dbs(self) -> list[str]:
        return self._mongo_client.list_database_names()

    def set_db(self, db: str) -> None:
        self.db = db

    def list_collections(self, db: str) -> list[str]:
        return self._mongo_client[db].list_collection_names()

    def getcollection(self, collection: str) -> Collection:
        return self._mongo_client[self.db][collection]
