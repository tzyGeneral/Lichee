import torch
from utils import binary_encode, fizz_buzz_encode

NUM_DIGITS = 10

trX = torch.Tensor([binary_encode(i, NUM_DIGITS) for i in range(101, 2 ** NUM_DIGITS)])  # 训练数据， 101致以上，好像是923个
trY = torch.LongTensor([fizz_buzz_encode(i) for i in range(101, 2 ** NUM_DIGITS)])  # x可以是float类型，但是y是表示类别的，不行


NUM_HIDDEN = 100
model = torch.nn.Sequential(    # 模型定义，激活函数为ReLU
    torch.nn.Linear(NUM_DIGITS, NUM_HIDDEN),
    torch.nn.ReLU(),
    torch.nn.Linear(NUM_HIDDEN, 4)
)

if torch.cuda.is_available():   # 模型转到gpu上运行
    model = model.cuda()


loss_fn = torch.nn.CrossEntropyLoss() # 损失函数使用交叉熵损失函数
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)   # 优化算法选择SGD，可百度下SGD，是随机梯度下降法，torch封装了好几个优化算法，可以自行试试

BATCH_SIZE = 128


def run():
    for epoch in range(10000):    # 训练epoch是1000， 视频上老师训练是10000，我嫌太大了，慢，所以改为了1000,但是效果确实不如10000的，可以自己试试
        for start in range(0, len(trX), BATCH_SIZE):   # 批量大小为BATCH_SIZE
            end = start + BATCH_SIZE
            batchX = trX[start:end]
            batchY = trY[start:end]

            if torch.cuda.is_available():   # 训练数据搬到gpu
                batchX = batchX.cuda()
                batchY = batchY.cuda()

            y_pred = model(batchX)

            loss = loss_fn(y_pred, batchY)
            print("Epoch", epoch, loss.item())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    torch.save(model, 'fbmodel.pkl')


if __name__ == '__main__':
    run()