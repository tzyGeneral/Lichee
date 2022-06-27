import grequests
import requests


def run():
    baseUrl = "http://kxcz.ycsw168.com/index/index/add.html"
    form = {
        "id": "8705001814383955",
        "password": "1234567890",
        "phone": "13878517612",
        "code": "NAKY",
        "time": "2022-02-11 11:41:13",
        "ip": "117.30.74.238-福建省"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Referer": "http://kxcz.ycsw168.com/qazxswz00"
    }
    proxies = {
        "http": "127.0.0.1:7890"
    }
    res = requests.post(baseUrl, headers=headers, data=form, proxies=proxies)
    print(res.text)
    data = []
    for one in range(100000):
        form["id"] = str(int(form["id"]) + one)
        data.append(grequests.post(baseUrl, headers=headers, data=form, proxies=proxies))

    print(data)
    res_list = grequests.map(data)
    print(res_list[0].text)



if __name__ == '__main__':
    run()



