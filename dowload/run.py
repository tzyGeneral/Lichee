import requests
import redis
import json
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def delete_dup(li: list):
    seen = set()
    new_list = []
    for d in li:
        d1 = d['id']
        if d1 not in seen:
            new_list.append(d)
            seen.add(d1)
    return new_list


def download_picture(name_url_dict: dict):
    """下载图片"""
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    # f"./marineserre/{note['liked_count']}_{note['id']}_{index}.png"

    with open(name_url_dict["path"], 'wb') as f:
        r = requests.get(name_url_dict["url"], headers=headers).content
        f.write(r)


def main():

    pool = redis.ConnectionPool(host='127.0.0.1', db=1, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    data = db.lrange("marineserre", 0, -1)
    res = []
    for one in data:
        one = json.loads(one)
        if not one["data"]: continue

        for shop in one["data"]["items"]:
            try:
                res.append(shop["note"])
            except KeyError:
                continue

    print(len(res))
    set_res = delete_dup(res)
    print(len(set_res))

    task = []
    for note in set_res:
        for index, im in enumerate(note["images_list"]):
            task.append(
                {
                    "path": f"./marineserre/{note['liked_count']}_{note['id']}_{index}.png",
                    "url": im["url_size_large"]
                }
            )
    # 利用多线程兵法下载
    executor = ThreadPoolExecutor(max_workers=10)
    future_tasks = [executor.submit(download_picture, t) for t in task]
    # 等待所有县城完成，在进入后续的执行
    wait(future_tasks, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    main()