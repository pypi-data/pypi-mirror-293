from os import getenv
from metamorfo.utility import hexa_b64

import redis


class RedisDatabase:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        connection_key = hexa_b64(str(kwargs))

        if connection_key not in cls._instances:
            cls._instances[connection_key] = super(__class__, cls).__new__(cls)
        return cls._instances[connection_key]

    def __init__(self, *args, **kwargs) -> None:
        self._connection_key = (
            args[0] if len(args) > 0 else hexa_b64(str(kwargs))
        )
        if kwargs == {}:
            user = getenv("METAMORFO_REDIS_USER")
            pssw = getenv("METAMORFO_REDIS_PASSWORD")
            host = getenv("METAMORFO_REDIS_HOST")
            port = getenv("METAMORFO_REDIS_PORT")
        else:
            user = kwargs["username"]
            pssw = kwargs["password"]
            host = kwargs["host"]
            port = kwargs["port"]
        self.__connect(user, pssw, host, port)

    def __connect(self, user, pssw, host, port):
        self._redis_client = redis.Redis(
            host=host,
            port=int(port),
            username=user,
            password=pssw,
            decode_responses=True,
            db=0,
        )

    def get(self, key):
        return self._redis_client.get(key)

    def set(self, key, value, expire=None):
        if expire:
            self._redis_client.setex(key, expire, value)
        else:
            self._redis_client.set(key, value)

    def ttl(self, key):
        return self._redis_client.ttl(key)

    def delete(self, key):
        self._redis_client.delete(key)
