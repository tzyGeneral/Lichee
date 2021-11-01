import base64
import time
import cv2
import numpy as np


def saveBase64ToPic(img_src: str):
    """存储base64格式图片到本地"""

    # img_src = base64.urlsafe_b64decode(img_src + '=' * (4 - len(img_src) % 4))
    img_name = str(int(time.time())) + '.jpg'
    print(img_src.split(','))
    img_src = img_src.split(',')[1]
    print(img_src + '=' * (4 - len(img_src) % 4))
    img_src = base64.urlsafe_b64decode(img_src + '=' * (4 - len(img_src) % 4))

    with open(img_name, 'wb') as f:
        f.write(img_src)


def slide_captcha():
    """缺口滑块"""
    bg = cv2.imread('img.png')
    front = cv2.imread('que.png')

    # 灰度处理
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    front = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)

    # 对缺口处理
    front = front[front.any(1)]

    result = cv2.matchTemplate(bg, front, cv2.TM_CCOEFF_NORMED)
    yiwei_max_loc = np.argmax(result)  # 返回矩阵的最大一维位置，但是我们需要二维的位置
    _, y = np.unravel_index(yiwei_max_loc, result.shape)  # 会将一维的位置逆向根据二维的形状，返回位置横纵坐标
    print(y)


# saveBase64ToPic("""data:image/png;base64,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%0AAElFTkSuQmCC""")
# slide_captcha()

a = """data:image/png;base64,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"""

b = """data:image/jpeg;base64,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"""


print(a.replace('\n', '').replace('\r', ''))
print(b)