import  numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE



if __name__ == "__main__":
    S = np.array([1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,2,3,4,1,4,1,1,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,2,3,4,1,4,1,1]).reshape(2,3,3,3)
    print(S)
    print('------------------------')
    print(S.sum(axis=0))

    day = '_resnet50vgg_max_0511'

    data = np.load('../dataXY' + day + '.npz')
    classes = data['y']
    temp = np.argmax(classes, axis=1)

    model = TSNE(learning_rate=100)
    transformed = model.fit_transform(data['x'])

    xs = transformed[:, 0]
    ys = transformed[:, 1]


    plt.scatter(xs, ys, c = temp)

    plt.show()



