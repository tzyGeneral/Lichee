import numpy as np


def binary_encode(i, num_digits):  # 转二进制计算
    return np.array([i >> d & 1 for d in range(num_digits)])[::-1]  # [::-1]是把arry倒过来，因为一开始转的是二进制反的


def fizz_buzz_encode(i):
    if i % 15 == 0:
        return 3
    elif i % 5 == 0:
        return 2
    elif i % 3 == 0:
        return 1
    else:
        return 0


def fizz_buzz_decode(i, prediction):
    return [str(i), 'fizz', 'buzz', 'fizzbuzz'][prediction]  # 这是个很好玩的用法，我也是第一次见，各位可以打印一下试试
