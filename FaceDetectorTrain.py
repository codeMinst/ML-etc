#다층 퍼셉트론 신경망 모델로 얼굴위치 추론 트레이닝
import numpy
from keras.models import Sequential
from keras.layers import Dense, Dropout
import os
from PIL import Image

trainPath = 'dataset/collection/train'
valPath = 'dataset/collection/val'
width = 224
height = 224

# 1. 데이터셋 생성하기
def generateXY(path):
    x_train, y_train = [], []
    dirs = os.listdir(path)
    for dir in dirs[:30]:
        if '.txt' in dir:
            continue
        txtPath = path + '/' + dir + '.txt'

        f = open(txtPath, 'r')
        for r in f.readlines():
            line = r[:-1].split(' ')
            position= line[1:]
            y_train.append(numpy.array(position))
            print(line)
        f.close()

        files = os.listdir(path + '/' + dir)
        for file in files:
            filePath = path + '/' + dir + '/' + file
            img = Image.open(filePath).convert('RGB')
            img = numpy.array(img) / 255.0
            x_train.append(img)
    return numpy.array(x_train), numpy.array(y_train)

if os.path.isfile("FDtrainXY.npz"):
    tr = numpy.load('FDtrainXY.npz')
    x_train, y_train = tr['x'], tr['y']
    va = numpy.load('FDvalXY.npz')
    x_val, y_val = va['x'], va['y']
else:
    x_train, y_train = generateXY(trainPath)
    numpy.savez('FDtrainXY' , x=x_train, y=y_train)
    x_val, y_val = generateXY(valPath)
    numpy.savez('FDvalXY' , x=x_val, y=y_val)

x_train = x_train.reshape(x_train.shape[0], width*height * 3)
x_val = x_val.reshape(x_val.shape[0], width*height * 3)

# 2. 모델 구성하기
model = Sequential()
model.add(Dense(256, activation='relu', input_dim = width*height*3))
model.add(Dense(256, activation='relu'))
model.add(Dense(256))
model.add(Dense(4))
#필터 너무커도 안됨
#드롭아웃은 많이 돌릴때 효율적

model.compile(loss='mse', optimizer='adam', metrics=['acc'])

hist = model.fit(x_train, y_train, batch_size=32, epochs=300, validation_data=(x_val, y_val))

score = model.evaluate(x_val, y_val, batch_size=32)
print(score)
model.save('face_detector_dnn.h5')