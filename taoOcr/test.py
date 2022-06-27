import requests

import ddddocr
import cv2

# det = ddddocr.DdddOcr(ocr=True, old=True)



headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
    "referer": "https://www.mozimh.com"
}

res = requests.get(
    url="https://pic.kkhmh.xyz/882/thumb.jpg",
    headers=headers
)

with open("home3.jpg", 'wb') as f:
    image = f.write(res.content)

# poses = det.classification(res.content)
# print(poses)
