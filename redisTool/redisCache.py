import redis

pool = redis.ConnectionPool(host='127.0.0.1')


class RedisDataBase:
    """将redis作为一个简单的key-value存储"""

    def __init__(self):
        self.__db = redis.Redis(connection_pool=pool)

    def setMany(self, dic: dict):
        """
        一次存储多个键值
        :param dic:
        :return:
        """
        self.__db.mset(dic)

    def getMany(self, keyList: list):
        """
        一次获取多个值
        :param keyList: 装有key的列表
        :return:
        """
        result = self.__db.mget(keyList)
        return result

    def setOne(self, dic: dict):
        """
        一次存储一个键值
        :param dic:
        :return:
        """
        key = tuple(dic.keys())[0]
        value = tuple(dic.values())[0]
        self.__db.set(str(key), value)

    def getOne(self, key: str):
        """
        一次获取一个值
        :param key:
        :return:
        """
        check = self.__db.exists(key)
        if check:
            result = self.__db.get(key)
            result = eval(result)
        else:
            result = []
        return result


