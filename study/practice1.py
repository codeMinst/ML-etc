import numpy as np
import matplotlib.pylab as plt

#step function
def step_finction(x):
    y = x > 0
    #convert a array data type
    return y.astype(np.int)

#sigmoid fuction
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

#sigmoid fuction
def relu(x):
    return np.maximum(0, x)

def indentity_function(x):
    return x

#왜 밑을 e인 자연로그함수를 사용하는가 하냐면 큰 수의 복잡한 계산을 할 때 계산을 단수화하기 위해서 사용
#특히 자연로그를 사용했을 때 미적분의 계산이 간편
#기울기를 계산하거나 오차역전파에 대한 계산을 할 때 미분을 사용
#자연로그(ln)의 역함수는 지수함수인 exp(x)
def softmax(a):
    c = np.max(a)
    exp = np.exp(a -c)
    exp_sum = np.sum(exp)
    y = exp / exp_sum

    return y

#creatre arry -5.0 ~ 5.0  by 0.1 interval
x = np.arange(-5.0, 5.0, 0.1)
y = step_finction(x)

plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()

y = sigmoid(x)
plt.plot(x, y)
plt.show()

y = relu(x)
plt.plot(x, y)
plt.show()

def init_network():
    netwrok = {}
    netwrok['W1'] = np.array([[0.1,0.3,0.5],[0.2,0.4,0.6]])
    netwrok['b1'] = np.array([[0.1, 0.2, 0.3]])
    netwrok['W2'] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
    netwrok['b2'] = np.array([[0.1, 0.2]])
    netwrok['W3'] = np.array([[0.1, 0.3], [0.2, 0.4]])
    netwrok['b3'] = np.array([[0.1, 0.2]])

    return netwrok

def forward(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = softmax(a3)

    return  y

x = np.array([1.0, 0.5])
network = init_network()
y= forward(network, x)
print(y)

