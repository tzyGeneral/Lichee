import ddddocr
import cv2

det = ddddocr.DdddOcr(det=True)

with open("home3.jpg", 'rb') as f:
    image = f.read()

poses = det.detection(image)


#
im = cv2.imread("home3.jpg")

for box in poses:
    x1, y1, x2, y2 = box
    im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

cv2.imwrite("result.jpg", im)