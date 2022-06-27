import numpy as np
import torch


random_num_list = [6, 1, 2, 9, 5, 7, 8, 2, 1, 3, 9, 4, 3, 6, 9, 10, 5, 2, 3, 9, 3, 10, 1, 3, 4, 6, 6, 6, 4, 5, 10, 5, 4, 4, 4, 8, 5, 9, 1, 2, 5, 3, 8, 5, 9, 5, 5, 6, 8, 9, 9, 6, 9, 4, 4, 5, 8, 10, 3, 1, 4, 5, 9, 2, 9, 8, 9, 5, 10, 6, 3, 8, 9, 2, 4, 4, 10, 3, 1, 5, 10, 9, 7, 1, 4, 8, 2, 3, 6, 6, 1, 5, 10, 6, 7, 9, 8, 6, 5, 5, 8, 2, 10, 8, 2, 1, 10, 3, 8, 9, 9, 2, 1, 3, 4, 1, 8, 10, 2, 10, 1, 3, 6, 6, 8, 4, 1, 7, 8, 5, 4, 6, 10, 5, 7, 9, 4, 4, 5, 6, 4, 5, 1, 4, 6, 4, 8, 8, 8, 6, 2, 1, 6, 1, 1, 7, 10, 1, 5, 9, 8, 8, 3, 5, 7, 1, 8, 6, 4, 9, 2, 2, 7, 8, 8, 8, 8, 6, 8, 5, 7, 3, 4, 9, 4, 3, 9, 10, 8, 1, 6, 2, 3, 1, 7, 2, 7, 2, 10, 3, 3, 1, 2, 1, 4, 8, 9, 3, 8, 7, 2, 10, 9, 9, 5, 3, 7, 3, 6, 10, 5, 6, 5, 1, 5, 2, 4, 1, 8, 6, 9, 2, 1, 2, 9, 9, 1, 10, 5, 8, 1, 3, 1, 8, 10, 9, 5, 5, 8, 3, 5, 10, 3, 1, 1, 5, 8, 1, 4, 3, 7, 10, 1, 5, 10, 5, 9, 3, 1, 3, 5, 7, 7, 1, 2, 10, 4, 5, 1, 1, 10, 9, 2, 9, 1, 10, 10, 3, 1, 8, 8, 5, 3, 4, 9, 7, 2, 9, 4, 9, 2, 2, 8, 5, 9, 2, 3, 7, 9, 3, 5, 3, 1, 8, 4, 6, 1, 4, 6, 9, 3, 9, 7, 1, 7, 3, 8, 2, 8, 8, 4, 8, 10, 9, 6, 8, 6, 10, 3, 4, 1, 4, 8, 4, 3, 2, 6, 2, 7, 8, 6, 3, 7, 1, 3, 3, 6, 3, 5, 6, 3, 6, 10, 2, 7, 5, 1, 7, 3, 5, 4, 2, 9, 5, 1, 8, 4, 2, 10, 1, 2, 6, 7, 9, 3, 5, 1, 8, 5, 4, 4, 2, 4, 9, 1, 7, 8, 6, 10, 10, 8, 8, 10, 5, 9, 2, 1, 9, 3, 2, 3, 10, 3, 8, 8, 7, 10, 3, 1, 7, 1, 5, 9, 10, 4, 9, 5, 1, 9, 8, 7, 4, 8, 2, 3, 6, 9, 5, 8, 8, 7, 6, 7, 4, 8, 6, 9, 5, 1, 6, 3, 10, 7, 6, 8, 6, 4, 5, 7, 2, 7, 8, 6, 3, 10, 3, 1, 6, 9, 1, 8, 6, 3, 5, 6, 6, 3, 3, 2, 7, 8, 8, 10, 2, 2, 9, 4, 9, 10, 6, 8, 1, 8, 3, 8, 6, 9, 9, 9, 10, 8, 3, 3, 5, 4, 10, 10, 3, 7, 1, 10, 3, 9, 1, 5, 2, 9, 6, 4, 6, 5, 6, 4, 5, 6, 5, 2, 2, 10, 8, 2, 10, 7, 8, 7, 9, 7, 6, 6, 4, 6, 1, 6, 1, 3, 5, 3, 10, 7, 6, 8, 2, 10, 7, 6, 4, 5, 6, 2, 1, 8, 5, 5, 9, 7, 6, 7, 9, 1, 5, 7, 4, 3, 4, 4, 10, 4, 2, 8, 4, 9, 6, 6, 8, 6, 10, 5, 1, 2, 6, 3, 6, 7, 3, 1, 10, 4, 1, 2, 4, 10, 7, 9, 2, 4, 7, 8, 1, 4, 4, 7, 7, 3, 7, 10, 8, 3, 9, 6, 10, 6, 1, 9, 8, 1, 6, 10, 8, 2, 8, 8, 5, 3, 3, 9, 3, 2, 8, 10, 2, 3, 4, 10, 10, 7, 1, 5, 3, 3, 6, 8, 5, 7, 10, 3, 7, 8, 4, 8, 2, 8, 7, 5, 3, 5, 2, 4, 7, 8, 7, 4, 8, 9, 6, 3, 10, 8, 6, 4, 1, 3, 6, 2, 3, 4, 8, 7, 3, 1, 10, 9, 1, 4, 4, 4, 7, 3, 1, 4, 8, 8, 2, 8, 6, 7, 2, 9, 6, 7, 4, 7, 6, 1, 10, 9, 3, 2, 1, 1, 6, 7, 7, 1, 3, 4, 9, 8, 7, 9, 3, 9, 10, 7, 8, 4, 3, 2, 5, 10, 4, 9, 3, 1, 1, 4, 9, 10, 9, 5, 4, 6, 6, 7, 1, 9, 6, 4, 8, 2, 6, 1, 5, 2, 9, 1, 10, 1, 5, 8, 3, 4, 1, 3, 1, 5, 9, 8, 5, 1, 9, 9, 1, 6, 10, 3, 6, 7, 7, 9, 2, 10, 9, 10, 7, 3, 8, 6, 7, 8, 1, 3, 9, 8, 3, 6, 3, 7, 8, 5, 9, 6, 3, 10, 5, 6, 10, 8, 4, 4, 1, 8, 3, 1, 6, 6, 7, 2, 9, 2, 4, 7, 9, 2, 9, 1, 8, 5, 7, 9, 2, 5, 7, 9, 5, 6, 2, 8, 4, 6, 8, 8, 1, 9, 5, 10, 6, 4, 2, 1, 2, 10, 2, 4, 2, 6, 7, 7, 2, 7, 5, 2, 2, 5, 8, 10, 2, 1, 1, 5, 7, 1, 5, 2, 9, 2, 4, 6, 9, 5, 6, 2, 2, 6, 7, 1, 6, 5, 8, 6, 3, 2, 1, 2, 8, 9, 9, 10, 1, 6, 3, 7, 6, 5, 5, 2, 10, 1, 9, 9, 1, 4, 9, 6, 9, 9, 6, 9, 3, 5, 1, 3, 9, 10, 3, 10, 7, 1, 4, 5, 9, 6, 3, 5, 3, 10, 9, 9, 7, 8, 4, 8, 10, 10, 10, 1, 8, 9, 2, 5, 1, 6, 4, 6, 9, 10, 10, 5, 6, 10, 8, 2, 4, 1, 4, 3, 4, 10, 7, 9, 1, 3, 3, 9, 2, 1, 9, 10, 3, 10, 6, 6, 2, 9, 4, 8, 1, 9, 1, 5, 5, 9, 10, 1, 3, 10, 4, 2, 7, 4, 7, 9, 6, 4, 10, 4, 9, 10, 3, 4, 6, 9, 3, 1, 9, 7, 1, 7, 5, 1, 9, 6, 10, 8, 1, 6, 6, 5, 5, 3, 2, 6, 4, 9, 5, 8, 5, 5, 8, 2, 4, 7, 9, 3, 8, 10, 5, 9, 9, 9, 7, 2, 2, 10, 9, 1, 6, 6, 3, 1, 5, 2, 3, 7, 4, 7, 4, 7, 9, 7, 9, 4, 1, 2, 9, 5, 2, 3, 6, 9, 5, 9, 6, 10, 1, 5, 7, 8, 5, 4, 10, 5, 2, 3, 4, 9, 9, 6, 1, 4, 3, 5, 7, 9, 5, 4, 8, 2, 9, 4, 8, 4, 9, 4, 10, 4, 9, 1, 2, 10, 10, 10, 9, 2, 7, 8, 1, 1, 2, 10, 7, 6, 3, 10, 5, 1, 10, 4, 4, 5, 8, 5, 1, 5, 2, 2, 3, 1, 4, 3, 9, 2, 5, 10, 2, 7, 9, 10, 7, 2, 2, 5, 1, 10, 5, 2, 2, 2, 9, 6, 9, 9, 10, 6, 9, 1, 5, 8, 4, 2, 8, 7, 10, 1, 1, 10, 10, 7, 8, 1, 2]

NUM_DIGITS = 10


def num_encode(i, num_digits):
    """
    num_digits: 随机数的总个数
    """
    return np.array([i >> d & 1 for d in range(num_digits)])[::-1]


trX = torch.Tensor([num_encode(i, NUM_DIGITS) for i in range(101, 2 ** NUM_DIGITS)])
trY = torch.LongTensor([random_num_list[i] for i in range(101, 2 ** NUM_DIGITS)])

NUM_HIDDEN = 100
model = torch.nn.Sequential(
    torch.nn.Linear(NUM_DIGITS, NUM_HIDDEN),
    torch.nn.ReLU(),
    torch.nn.Linear(NUM_HIDDEN, 11)
)

if torch.cuda.is_available():
    model = model.cuda()


loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

BATCH_SIZE = 128


def train():
    for epoch in range(10000):
        for start in range(0, len(trX), BATCH_SIZE):
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

    torch.save(model, 'random_num.pkl')


if __name__ == '__main__':
    train()