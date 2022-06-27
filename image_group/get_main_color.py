import cv2
import os
import numpy as np
from skimage import io
from sklearn.cluster import KMeans

image_path = []


images = os.listdir("./unit6/fontimages/a_thumbs")

for image_name in images:
    image_path.append('./unit6/fontimages/a_thumbs/' + image_name)

for path in image_path[:1]:
    img = cv2.imread(path)
    img1 = img.reshape((img.shape[0] * img.shape[1], img.shape[2]))

    # 聚类个数
    k = 3
    # 构造聚类器
    estimator = KMeans(n_clusters=k, max_iter=4000, init='k-means++', n_init=50)
    # 聚类
    estimator.fit(img1)
    # 获取聚类中心
    centroids = estimator.cluster_centers_

    # 使用算法跑出的中心点，生成一个矩阵，为数据可视化做准备
    result = []
    result_width = 200
    result_height_per_center = 80
    # 获取图片色彩层数
    n_channels = img1.shape[1]

    for center_index in range(k):
        result.append(
            np.full((result_width * result_height_per_center, n_channels), centroids[center_index], dtype=int))

    result = np.array(result)
    result = result.reshape((result_height_per_center * k, result_width, n_channels))
    result = result.astype(np.uint8)
    cv2.imshow('maincolor', result)
    cv2.waitKey(0)
    # 保存图片
