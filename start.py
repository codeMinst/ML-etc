import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pylab as plt
from matplotlib.image import imread
# 랜덤시드 고정시키기
#np.random.seed(3)

# 1. 이미지 용도별 제네레이터 생성
train_datagen = ImageDataGenerator(rescale=1./255)#rgb값 reduce
train_generator = train_datagen.flow_from_directory(
        '../dataset/furuit/train',
        target_size=(24, 24),
        batch_size=10,
        class_mode='categorical')

val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
        '../dataset/furuit/validation',
        target_size=(24, 24),
        batch_size=10,
        class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        '../dataset/furuit/test',
        target_size=(24, 24),
        batch_size=10,
        class_mode='categorical')

# 2. 모델 구성
model = Sequential()
#conv필터 수, 커널크기, activation funtion, 샘플 입력형태(첫레이어에서만 정의)
#레이어의 conv필터 수는 (다음레이어에서 쓰이는)피쳐맵의 채널
#3 (k)* 3(k) * 3(i) * 32(o) +32(o) = param(896 wb)
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(24,24,3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))

model.summary()

# 3. 모델 학습과정 설정
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 4. 모델 학습
model.fit_generator(
        train_generator,
        steps_per_epoch=75,
        epochs=15,
        validation_data=val_generator,
        validation_steps=15)

# 6. 모델 평가
print("-- Evaluate --")
scores = model.evaluate_generator(val_generator, steps=5)
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))

# 7. 모델 사용하기
print("-- Predict --")
output = model.predict_generator(test_generator, steps=5)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(test_generator.class_indices)
print(output)