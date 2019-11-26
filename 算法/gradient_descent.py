"""
实现梯度下降算法以最小化线性假设函数的成本。
"""
import numpy

# List of input, output pairs
train_data = (
    ((5, 2, 3), 15),
    ((6, 5, 9), 25),
    ((11, 12, 13), 41),
    ((1, 1, 1), 8),
    ((11, 12, 13), 41),
)
test_data = (((515, 22, 13), 555), ((61, 35, 49), 150))
parameter_vector = [2, 4, 1, 5]
m = len(train_data)
LEARNING_RATE = 0.009


def _error(example_no, data_set="train"):
    """
    :param data_set: 训练数据或测试数据
    :param example_no: 必须检查其错误的示例编号
    :return: 示例编号所指出的示例错误。
    """
    return calculate_hypothesis_value(example_no, data_set) - output(
        example_no, data_set
    )


def _hypothesis_value(data_input_tuple):
    """
    计算给定输入的假设函数值
    :param data_input_tuple: 特定示例的输入元组
    :return: 假设函数的值。
    请注意，存在一个“偏置输入”，其值固定为1。
    输入数据中未明确提及。但是，ML假设函数使用它。
    因此，我们必须单独处理它。第36行负责此事。
    """
    hyp_val = 0
    for i in range(len(parameter_vector) - 1):
        hyp_val += data_input_tuple[i] * parameter_vector[i + 1]
    hyp_val += parameter_vector[0]
    return hyp_val


def output(example_no, data_set):
    """
    :param data_set: 测试数据或训练数据
    :param example_no: 要获取其输出的示例
    :return: 该示例的输出
    """
    if data_set == "train":
        return train_data[example_no][1]
    elif data_set == "test":
        return test_data[example_no][1]


def calculate_hypothesis_value(example_no, data_set):
    """
    计算给定示例的假设值
    :param data_set: 测试数据或train_data
    :param example_no: 要计算其假设值的示例
    :return: 该示例的假设值
    """
    if data_set == "train":
        return _hypothesis_value(train_data[example_no][0])
    elif data_set == "test":
        return _hypothesis_value(test_data[example_no][0])


def summation_of_cost_derivative(index, end=m):
    """
    计算成本函数导数之和
    :param index: 正在计算索引wrt导数
    :param end: 求和结束的值，默认为m，示例数
    :return: 返回成本导数的总和
    注意：如果index为-1，则意味着我们正在计算偏差参数的总和。
    """
    summation_value = 0
    for i in range(end):
        if index == -1:
            summation_value += _error(i)
        else:
            summation_value += _error(i) * train_data[i][0][index]
    return summation_value


def get_cost_derivative(index):
    """
    :param index: 要计算参数向量wrt到导数的索引
    :return: 该索引的导数wrt
    注意：如果index为-1，则意味着我们正在计算偏差参数的总和。
    """
    cost_derivative_value = summation_of_cost_derivative(index, m) / m
    return cost_derivative_value


def run_gradient_descent():
    global parameter_vector
    # 调整这些值以设置预测输出的公差值
    absolute_error_limit = 0.000002
    relative_error_limit = 0
    j = 0
    while True:
        j += 1
        temp_parameter_vector = [0, 0, 0, 0]
        for i in range(0, len(parameter_vector)):
            cost_derivative = get_cost_derivative(i - 1)
            temp_parameter_vector[i] = (
                parameter_vector[i] - LEARNING_RATE * cost_derivative
            )
        if numpy.allclose(
            parameter_vector,
            temp_parameter_vector,
            atol=absolute_error_limit,
            rtol=relative_error_limit,
        ):
            break
        parameter_vector = temp_parameter_vector
    print(("迭代次数:", j))


def test_gradient_descent():
    for i in range(len(test_data)):
        print(("实际输出值:", output(i, "test")))
        print(("假设输出:", calculate_hypothesis_value(i, "test")))


if __name__ == "__main__":
    run_gradient_descent()
    print("\n测试线性假设函数的梯度下降。\n")
    test_gradient_descent()