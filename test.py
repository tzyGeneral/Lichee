import time


def timmer(func):
    # 传入的参数是一个函数
    def deco(*args, **kwargs):
        # 本应传入运行函数的各种参数
        print('\n函数：{_funcname_}开始运行：'.format(_funcname_=func.__name__))
        start_time = time.time()
        # 调用代运行的函数，并将各种原本的参数传入
        res = func(*args, **kwargs)
        end_time = time.time()
        print('函数:{_funcname_}运行了 {_time_}秒'
              .format(_funcname_=func.__name__, _time_=(end_time - start_time)))
        # 返回值为函数的运行结果
        return res

    # 返回值为函数
    return deco


@timmer
def test1():
    a = []
    new = []
    for i in range(1000000):
        a.append(
            {"nameA": i,
             "nameB": i,
             "nameC": i,
             "nameD": i}
        )

    for one in a:
        new.append({"name2": one["nameA"]})
        new.append({"name3": one["nameB"]})
        new.append({"name4": one["nameC"]})
        new.append({"name5": one["nameD"]})

@timmer
def test2():
    a = []
    for i in range(1000000):
        a.append(
            {"nameA": i,
             "nameB": i,
             "nameC": i,
             "nameD": i}
        )

    def func(one: dict):
        one["name2"] = one.pop("nameA")
        one["name3"] = one.pop("nameB")
        one["name4"] = one.pop("nameC")
        one["name5"] = one.pop("nameD")

    list(map(func, a))

class Single(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass









