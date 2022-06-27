import torch
from utils import binary_encode, fizz_buzz_decode


model = torch.load('./fbmodel.pkl')

NUM_DIGITS = 10

testX = torch.Tensor([binary_encode(i, NUM_DIGITS) for i in range(1, 101)])
if torch.cuda.is_available():
    testX = testX.cuda()


with torch.no_grad():
    testY = model(testX)

predictions = zip(range(1, 101), testY.max(1)[1].cpu().data.tolist())      # 非常有意思和技巧的一个东西，testY.max(1)[1].cpu().data.tolist()可以自己试试，打印
print([fizz_buzz_decode(i, x) for i, x in predictions])