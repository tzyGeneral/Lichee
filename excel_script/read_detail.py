import json
import time
from pprint import pprint
from collections import Counter
import jieba
import xlrd
import requests
import redis
import xlsxwriter as xw


def write_excel(data_list: list, index: int):
    work_book = xw.Workbook(f"shope_{index}.xlsx")
    work_sheet = work_book.add_worksheet("sheet1")
    work_sheet.activate()

    title = list(data_list[0].keys())
    work_sheet.write_row('A1', title)
    i = 2
    for on in data_list:
        insert_data = list(on.values())
        row = 'A' + str(i)
        work_sheet.write_row(row, insert_data)
        i += 1
    work_book.close()


def delete_dup(li: list):
    seen = set()
    new_list = []
    for d in li:
        d1 = d['url']
        if d1 not in seen:
            new_list.append(d)
            seen.add(d1)
    return new_list


def check_brand(title: str):
    """确认品牌"""
    brand = ""
    if "done" in title.lower():
        brand = "we11done"

    elif "serre" in title.lower():
        brand = "Marine_serre"

    elif "eenk" in title.lower():
        brand = "eenk"

    return brand

def xiaohongshu():
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }

    def delete_dup(li: list):
        seen = set()
        new_list = []
        for d in li:
            d1 = d['id']
            if d1 not in seen:
                new_list.append(d)
                seen.add(d1)
        return new_list

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
    for note in set_res:
        for index, im in enumerate(note["images_list"]):
            print(im["url_size_large"])

            if not im["url_size_large"]:
                continue

            with open(f"./marineserre/{note['liked_count']}_{note['id']}_{index}.png", 'wb') as f:

                r = requests.get(im["url_size_large"], headers=headers).content

                f.write(r)




def run():
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    pool = redis.ConnectionPool(host='127.0.0.1', db=1, decode_responses=True)
    db = redis.Redis(connection_pool=pool)

    data = db.lrange("chao_detail_data", 0, -1)
    res = []
    for one in data:
        one = json.loads(one)
        if not one["data"]: continue
        try:
            item = one["data"]["item"]
            seller = one["data"]["seller"]
            apiStack = one["data"]["apiStack"]

            images = item["images"]  # 图片


            item_id = item["itemId"]
            title = item["title"]
            comment_count = item["commentCount"]  # 评论数
            favcount = item["favcount"]  # 收藏数
            brand = check_brand(title)

            shop_name = seller["shopName"]  # 店铺名
            shop_url = seller["taoShopUrl"]

            api_stack = json.loads(apiStack[0]["value"])
            price = api_stack["global"]["data"]["priceSectionData"]["price"]["priceText"]  # 原价
            extra_price = api_stack["global"]["data"]["priceSectionData"]["extraPrice"]["priceText"]  # 用券后价格

            sell_count = api_stack["global"]["data"]["item"].get("vagueSellCount")
            if not sell_count:
                sell_count = 0
            video_list = api_stack["global"]["data"]["item"].get("videos")
            if video_list:
                video = video_list[0]["url"]
            else:
                video = ""

            sku: dict = api_stack["global"]["data"]["skuCore"]["sku2info"]
            count = 0
            for s in sku.values():
                count += int(s["quantity"])

            for index, im in enumerate(images):
                with open(f"./image/{brand}_{sell_count}_{price}_{item_id}_{index}.png", 'wb') as f:
                    if "http" in im:
                        im_url = im
                    else:
                        im_url = "https:" + im
                    print(im_url)
                    r = requests.get(im_url, headers=headers).content
                    f.write(r)

            res.append(
                {
                    "图片": json.dumps(images),
                    "item_id": item_id,
                    "title": title,
                    "评论数": comment_count,
                    "收藏数": favcount,
                    "品牌": brand,
                    "shop_name": shop_name,
                    "shop_url": shop_url,
                    "原价": price,
                    "券后价格": extra_price,
                    "库存": count,
                    "月销量": sell_count,
                    "视频": video
                }
            )
        except KeyError as e:
            print(e)


    write_excel(res, 1)





if __name__ == '__main__':
    xiaohongshu()
