import numpy as np

NUM_DIGITS = 10

def binary_encode(i, num_digits):   # 转二进制计算
    return np.array([i >> d & 1 for d in range(num_digits)])[::-1]   # [::-1]是把arry倒过来，因为一开始转的是二进制反的

a = [binary_encode(i, NUM_DIGITS) for i in range(101, 2 ** NUM_DIGITS)]
print(a)