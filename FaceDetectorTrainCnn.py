#다층 퍼셉트론 신경망 모델로 얼굴위치 추론 트레이닝
import numpy
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
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
    for dir in dirs[:20]:
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

#dnn모델 구성
model = Sequential()
model.add(Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(width, height, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4))

#cnn + dnn
#내가 의도 한대로 구조가 안 나옴 패딩을 넣어야 하나?
'''
model = Sequential()
model.add(Conv2D(64, (3, 3),padding='same', activation='relu', input_shape=(width, height, 3)))
model.add(Conv2D(64, (3, 3),padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(128, (3, 3),padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(256, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(256, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(256, (3, 3),padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(512, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(512, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(512, (3, 3),padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(512, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(512, (3, 3),padding='same', activation='relu'))
model.add(Conv2D(512, (3, 3),padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4))
'''

model.summary()

model.compile(loss='mse', optimizer='adam', metrics=['acc'])

hist = model.fit(x_train, y_train, batch_size=32, epochs=200, validation_data=(x_val, y_val))

score = model.evaluate(x_val, y_val, batch_size=32)
print(score)
model.save('face_detector_model_vgg1.h5')