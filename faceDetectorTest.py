import numpy
from keras.models import load_model


va = numpy.load('../numpyz/FDvalXY.npz')
x_val, y_val = va['x'], va['y']
myModel = load_model('../weight/face_detector_model_vgg1.h5')
myModel.summary()
result = myModel.predict(x_val[0].reshape(1, 224, 224, 3))
#result = myModel.predict(x_val[0].reshape(-1, 224, 224, 3))

i = 0
for r in result:
    print("data ")
    print(y_val[i])
    print("result ")
    print(result[i])
    print("----------------------------------------------------------")
    i = i + 1