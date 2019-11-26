"""
基本回归决策时的实现
输入数据集：输入的数据集必须是一维且带有连续标签
输出：决策树将实数输入映射到实时输出
"""
import numpy as np


class Decision_Tree:
    def __init__(self, depth=5, min_leaf_size=5):
        self.depth = depth
        self.decision_boundary = 0
        self.left = None
        self.right = None
        self.min_leaf_size = min_leaf_size
        self.prediction = None

    def mean_squared_error(self, labels, prediction):
        """
        :param labels: 一维numpy数组a
        :param prediction: 浮点值
        :return: 如果使用预测来估计标签，则men——squared_error将计算错误
        >>> tester = Decision_Tree()
        >>> test_labels = np.array([1,2,3,4,5,6,7,8,9,10])
        >>> test_prediction = np.float(6)
        >>> assert tester.mean_squared_error(test_labels, test_prediction) == Test_Decision_Tree.helper_mean_squared_error_test(test_labels, test_prediction)
        >>> test_labels = np.array([1,2,3])
        >>> test_prediction = np.float(2)
        >>> assert tester.mean_squared_error(test_labels, test_prediction) == Test_Decision_Tree.helper_mean_squared_error_test(test_labels, test_prediction)
        """
        if labels.ndim != 1:
            print("Error: Input labels must be one dimensional")
        return np.mean((labels - prediction) ** 2)

    def train(self, X, y):
        """
        train y的内容是对应的X值的标签
        :param X: 一维numpy数组
        :param y: 一维numpy数组
        :return:
        """

        # 检查输入是否符合尺寸约束

        if X.ndim != 1:
            print("Error: Input data set must be one dimensional")
        if len(X) != len(y):
            print("Error: X and y have different lengths")
        if y.ndim != 1:
            print("Error: Data set labels must be one dimensional")
            return

        if len(X) < 2 * self.min_leaf_size:
            self.prediction = np.mean(y)
            return

        if self.depth == 1:
            self.prediction = np.mean(y)
            return

        if self.depth == 1:
            self.prediction = np.mean(y)
            return

        best_split = 0
        min_error = self.mean_squared_error(X, np.mean(y)) * 2

        # 循环遍历决策树的所有可能差分，找到最好的分裂。如果不存在小于2*的整个数组错误
        # 则不差分数据集，并将真个数组的平均值用作预测变量
        for i in range(len(X)):
            if len(X[:i]) < self.min_leaf_size:
                continue
            elif len(X[i:]) < self.min_leaf_size:
                continue
            else:
                error_left = self.mean_squared_error(X[:i], np.mean(y[:i]))
                error_right = self.mean_squared_error(X[i:], np.mean(y[i:]))
                error = error_left + error_right
                if error < min_error:
                    best_split = i
                    min_error = error

        if best_split != 0:
            left_X = X[:best_split]
            left_y = y[:best_split]
            right_X = X[best_split:]
            right_y = y[best_split:]

            self.decision_boundary = X[best_split]
            self.left = Decision_Tree(
                depth=self.depth - 1, min_leaf_size=self.min_leaf_size
            )
            self.right = Decision_Tree(
                depth=self.depth - 1, min_leaf_size=self.min_leaf_size
            )
            self.left.train(left_X, left_y)
            self.right.train(right_X, right_y)
        else:
            self.prediction = np.mean(y)

        return

    def predict(self, x):
        """
        预测函数通过递归调用预测函数来工作
        基于树的决策边界确定适当的子树
        :param x: 预测标签的浮点值
        :return:
        """
        if self.prediction is not None:
            return self.prediction
        elif self.left or self.right is not None:
            if x >= self.decision_boundary:
                return self.right.predict(x)
            else:
                return self.left.predict(x)
        else:
            print("Error: Decision tree not yet trained")
            return None


class Test_Decision_Tree:
    @staticmethod
    def helper_mean_squared_error_test(labels, prediction):
        """

        :param labels: 一维numpy数组
        :param prediction: 浮点值
        :return: helper_mean_squared_error_test计算均方误差
        """
        squared_error_sum = np.float(0)
        for label in labels:
            squared_error_sum += (label - prediction) ** 2

        return np.float(squared_error_sum / labels.size)


def main():
    """
    我们从numpy中的sin函数生成示例数据集。
    然后，我们在数据集上训练决策树，并使用决策树来预测10个不同测试值的标签。然后显示该测试的均方误差。
    :return:
    """
    X = np.arange(-1.0, 1.0, 0.005)
    y = np.sin(X)
    y = np.cos(X)

    tree = Decision_Tree(depth=10, min_leaf_size=10)
    tree.train(X, y)

    test_cases = (np.random.rand(10) * 2) - 1

    predictions = np.array([tree.predict(x) for x in test_cases])
    avg_error = np.mean((predictions - test_cases) ** 2)

    print("Test values: " + str(test_cases))
    print("Predictions: " + str(predictions))
    print("Average error: " + str(avg_error))


if __name__ == "__main__":
    main()
    import doctest

    doctest.testmod(name="mean_squarred_error", verbose=True)
