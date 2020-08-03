import redis


pool = redis.ConnectionPool(host='127.0.0.1')


class RedisZset:
    """用redis实现一个排行榜"""

    def __init__(self, name: str):
        self.__db = redis.Redis(connection_pool=pool)
        self.name = name

    def zadd(self, mapping: dict):
        """添加一个或多个成员，或者更新已存在成员的分数"""
        self.__db.zadd(self.name, mapping)

    def zincrby(self, soure: int, key: str):
        """
        增减成员分数
        :param soure: 分数：再次请求加1分（默认为1）
        :param key: 玩家key，没有则新增
        """
        self.__db.zincrby(self.name, soure, key)

    def zscore(self, key: str):
        """查看成员分数"""
        score = self.__db.zscore(self.name, key)
        return score

    def zrevrank(self, key: str):
        """查看成员的排名"""
        rank = self.__db.zrevrank(self.name, key)
        return rank

    def zrevrange(self):
        """查看排行榜"""
        rankPage = self.__db.zrevrange(self.name, 0, -1)
        rankPage = [x.decode('utf-8') for x in rankPage]
        return rankPage

    def zrem(self, key: str):
        """移除某个成员"""
        self.__db.zrem(self.name, key)

    def delZset(self):
        """删除排行榜"""
        self.__db.delete(self.name)

