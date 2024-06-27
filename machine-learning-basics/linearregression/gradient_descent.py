import pandas as pd
import numpy as np
from sklearn import linear_model
from math import isclose


df = pd.read_csv('test_scores.csv')

x_list = np.array(df['math'])
y_list = np.array(df['cs'])


def gradient_descent(x, y):
    m = 0
    b = 0
    n = len(x)
    iterations = 300000
    learning_rate = 0.0002
    cost_previous = 0
    for i in range(iterations):
        y_predict = m*x + b
        cost = sum((y - y_predict)**2)
        # print(f"m: {m} b: {b} cost: {cost}")
        if isclose(cost, cost_previous):
            break
        dm = (-2/n) * sum(x * (y - y_predict))
        db = (-2/n) * sum(y - y_predict)
        m = m - learning_rate * dm
        b = b - learning_rate * db

    return m, b


def sklearn_predict(x, y):
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    return regr.coef_, regr.intercept_


m_gradient, b_gradient = gradient_descent(x_list, y_list)
m_sklearn, b_sklearn = sklearn_predict(x_list.reshape(-1, 1), y_list)

print(f"Gradient descent algorithm, m:{m_gradient} b:{b_gradient}")
print(f"sklearn, m:{m_sklearn} b:{b_sklearn}")
