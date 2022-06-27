import os
import numpy as np
from sklearn.cluster import KMeans
import cv2
import torch.nn as nn
import torchvision.models as models
from imutils import build_montages
from PIL import Image
from torchvision import transforms
import matplotlib.image as imgplt


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        resnet50 = models.resnet50(pretrained=True)
        self.resnet = nn.Sequential(resnet50.conv1,
                                    resnet50.bn1,
                                    resnet50.relu,
                                    resnet50.maxpool,
                                    resnet50.layer1,
                                    resnet50.layer2,
                                    resnet50.layer3,
                                    resnet50.layer4)

    def forward(self, x):
        x = self.resnet(x)
        return x

# net = Net().eval()


image_path = []
all_image = []
images = os.listdir("./unit6/fontimages/a_thumbs")

for image_name in images:
    image_path.append('./unit6/fontimages/a_thumbs/' + image_name)

for path in image_path:
    image = imgplt.imread(path)
    image = image.reshape(-1, )
    all_image.append(image)

clt = KMeans(n_clusters=3)
clt.fit(all_image)
label_ids = np.unique(clt.labels_)

for label_id in label_ids:
    idxs = np.where(clt.labels_ == label_id)[0]
    idxs = np.random.choice(idxs, size=min(25, len(idxs)), replace=False)
    sho_box = []
    for i in idxs:
        image = cv2.imread(image_path[i])

        sho_box.append(image)
    montage = build_montages(sho_box, (25, 25), (5,5))[0]

    title = "Type {}".format(label_id)
    cv2.imshow(title, montage)
    cv2.waitKey(0)


