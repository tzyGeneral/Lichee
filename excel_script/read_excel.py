import json
import time
from pprint import pprint
from collections import Counter
import jieba
import xlrd
import xlsxwriter as xw


def read_excel(file_path: str):
    excel = xlrd.open_workbook(file_path)
    sheet = excel.sheet_by_index(0)

    filter_list = []
    with open("/Users/tangzhenyuan/Library/Containers/com.tencent.WeWorkMac/Data/Documents/Profiles/A7974F61A840F61684D184C344F0920F/Caches/Files/2022-02/880a38e218e41cd4bb01b6fbe9189c1f/新建文本文档.txt", 'r') as f:
        d = f.readlines()
        for one in d:
            if not one: continue
            filter_list.append(one.strip())

    result = []
    for n in range(0, sheet.nrows):
        row_list = sheet.row_values(n)
        for i in filter_list:
            if i in row_list[0]:
                print(row_list[0], i)
                result.append(row_list[0])
                break
    return result



def write_excel(data_list: list, index: int):
    work_book = xw.Workbook(f"keyword_{index}.xlsx")
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

if __name__ == '__main__':
    # file_path = "/Users/tangzhenyuan/Library/Containers/com.tencent.WeWorkMac/Data/Documents/Profiles/A7974F61A840F61684D184C344F0920F/Caches/Files/2022-02/5d9e1aa7618609f51e9322caff0e66b7/淘宝什么筛词.xlsx"
    # result = read_excel(file_path)
    # write_excel(result)

    import redis

    pool = redis.ConnectionPool(host='127.0.0.1', db=1, decode_responses=True)
    db = redis.Redis(connection_pool=pool)

    data = db.lrange("chao_shop_data_2", 0, -1)

    d = []

    for one in data:
        one = json.loads(one)
        if not one["data"].get("itemsArray"):


            continue
        for de in one["data"]["itemsArray"]:
            # if not de.get("nick"):
            #
            #     break
            # print(json.dumps(one["data"]))

            dic = {
                        "price": de["price"],
                        "sales": de["sold"],
                        "title": de["title"],
                        # "nick": de["nick"],
                        "url": f"https://detail.tmall.com/item.htm?id={de['item_id']}"
                    }
            d.append(dic)

    res = delete_dup(d)


    res_de = []
    for i in res:
        if i["sales"] == "" or int(i["sales"]) <= 5:
            continue
        if "done" in i["title"].lower():
            i["brand"] = "we11done"
            res_de.append(i)
        elif "serre" in i["title"].lower():
            i["brand"] = "Marine serre"
            res_de.append(i)
        elif "eenk" in i["title"].lower():
            i["brand"] = "eenk"
            res_de.append(i)

    text = ""
    for a in [x for x in res_de if x["brand"] == "eenk"]:
        text += a["title"]

    seg_list = jieba.cut(text)
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    l = []
    for (k, v) in c.most_common(100):
        l.append(
            {
                "key": k,
                "num": v
            }
        )

    write_excel(l, "eenk")

    # res = []
    # for i in d:
    #     for de in i["data"]["itemsArray"]:
    #         res.append(
    #             {
    #                 "price": de["price"],
    #                 "sales": de["sold"],
    #                 "title": de["title"],
    #                 "nick": de["nick"],
    #                 "url": f"https://detail.tmall.com/item.htm?id={de['item_id']}"
    #             }
    #         )
    # print(res)
    # write_excel(res, 12)

    # data = db.smembers("yamaxun:result")
    #
    # def splitList(initList: list, childernListLen: int) -> list:
    #     """
    #     将列表分割为指定大小的小列表
    #     :param initList: 待分割的原始列表
    #     :param childernListLen: 分割大小
    #     :return:
    #     """
    #     list_of_group = zip(*(iter(initList),) * childernListLen)
    #     end_list = [list(i) for i in list_of_group]
    #     count = len(initList) % childernListLen
    #     end_list.append(initList[-count:]) if count != 0 else end_list
    #     return end_list
    # data_list = splitList(list(data), 50000)
    # for index, one in enumerate(data_list):
    #     write_excel(one, index)