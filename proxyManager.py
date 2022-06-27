import time
import json
import redis
import datetime
import requests


class Config:
    redis_conf = {
        "host": "127.0.0.1",
        "port": 6379,
        "password": "",
        "db": 0,
        "proxy_key": "proxy:pool"
    }


class ProxyManager:

    def __init__(self):
        self.config = Config
        self.redis_config = self.config.redis_conf
        self.clict = redis.Redis(host=self.redis_config["host"], port=self.redis_config["port"],
                                 password=self.redis_config["password"], db=self.redis_config["db"])
        self.instance_dict = {}

    def read_ip(self):
        try:
            resp = requests.get("https://tb.aoomao.com/taskapi/ping/ppp").json()
            proxy_dic: dict = resp["result"]["data"]
        except Exception as e:
            proxy_dic = {}
        result = []
        for one in proxy_dic.keys():
            result.append(f"{one}:8000")
        return result

    def delete_ip(self, live_ips, pool_ips):
        ip_to_removed = set(pool_ips) - set(live_ips)
        if ip_to_removed:
            self.clict.hdel(self.redis_config["proxy_key"], *list(ip_to_removed))

    def add_new_ips(self, live_ips, pool_ips):
        ip_to_add = set(live_ips) - set(pool_ips)
        if ip_to_add:
            ips = {}
            for ip in ip_to_add:
                ips[ip] = json.dumps({"private_ip": ip, "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            self.clict.hset(self.redis_config["proxy_key"], mapping=ips)

    def run(self):
        while True:
            live_ips = self.read_ip()
            pool_ips = [x.decode() for x in self.clict.hgetall(self.redis_config["proxy_key"])]
            self.delete_ip(live_ips, pool_ips)
            self.add_new_ips(live_ips, pool_ips)
            print("================")
            time.sleep(60)


if __name__ == '__main__':
    manager = ProxyManager()
    manager.run()