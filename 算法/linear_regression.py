"""
线性回归是最常用于回归的最基本类型
预测分析。这个想法很简单，我们有一个数据集，我们有
与功能相关联。功能应谨慎选择
根据他们的判断，我们的模型将能够做出多大的未来预测。
我们尝试在多次迭代中设置这些功能权重，以使其最佳
适合我们的数据集。在此特定代码中，我使用了CSGO数据集（ADR与
评分）。我们尝试最好地拟合数据集中的一条线并估计参数。
"""
import requests
import numpy as np
import time


def collect_dataset():
    """ Collect dataset of CSGO
    数据集包含ADR与玩家评分
    :return : 从链接获得的数据集，作为矩阵
    """
    response = requests.get(
        "https://raw.githubusercontent.com/yashLadha/"
        + "The_Math_of_Intelligence/master/Week1/ADRvs"
        + "Rating.csv"
    )
    lines = response.text.splitlines()
    data = []
    for item in lines:
        item = item.split(",")
        data.append(item)
        print(item)
        print('==========')
    data.pop(0)  # This is for removing the labels from the list
    dataset = np.matrix(data)
    return dataset


def run_steep_gradient_descent(data_x, data_y, len_data, alpha, theta):
    """ 运行梯度下降并相应地更新特征向量_
    :param data_x   : 包含数据集
    :param data_y   : 包含与每个数据条目关联的输出
    :param len_data : 数据长度
    :param alpha    : 模型的学习率
    :param theta    : 特征向量（我们模型的权重）
    ;param return    : Updated Feature's, using
                       curr_features - alpha_ * gradient(w.r.t. feature)
    """
    n = len_data

    prod = np.dot(theta, data_x.transpose())
    prod -= data_y.transpose()
    sum_grad = np.dot(prod, data_x)
    theta = theta - (alpha / n) * sum_grad
    return theta


def sum_of_square_error(data_x, data_y, len_data, theta):
    """ 返回平方误差之和以进行误差计算
    :param data_x    : 包含我们的数据集
    :param data_y    : 包含输出（结果向量）
    :param len_data  : 数据集的len
    :param theta     : 包含特征向量
    :return          : 从给定特征的平方误差之和
    """
    prod = np.dot(theta, data_x.transpose())
    prod -= data_y.transpose()
    sum_elem = np.sum(np.square(prod))
    error = sum_elem / (2 * len_data)
    return error


def run_linear_regression(data_x, data_y):
    """ 对数据集实施线性回归
    :param data_x  : 包含我们的数据集
    :param data_y  : 包含输出（结果向量）
    :return        : 最佳拟合线的特征（特征向量）
    """
    iterations = 100000
    alpha = 0.0001550

    no_features = data_x.shape[1]
    len_data = data_x.shape[0] - 1

    theta = np.zeros((1, no_features))

    for i in range(0, iterations):
        theta = run_steep_gradient_descent(data_x, data_y, len_data, alpha, theta)
        error = sum_of_square_error(data_x, data_y, len_data, theta)
        print("At Iteration %d - Error is %.5f " % (i + 1, error))

    return theta


def main():
    """ Driver function """
    data = collect_dataset()

    len_data = data.shape[0]
    data_x = np.c_[np.ones(len_data), data[:, :-1]].astype(float)
    data_y = data[:, -1].astype(float)

    theta = run_linear_regression(data_x, data_y)
    len_result = theta.shape[1]
    print("Resultant Feature vector : ")
    for i in range(0, len_result):
        print("%.5f" % (theta[0, i]))


if __name__ == "__main__":
    main()
