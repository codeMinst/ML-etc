import numpy as np
import os
import pickle
from usol import usolUtil
from usol import deep
'''
def transToNpy(tempFeatures, temlpLabel):
    features = np.zeros(shape=(tempFeatures.__len__(), 128))
    i = 0
    for fe in tempFeatures:
        features[i] = fe;
        i = i + 1
    labels = np.zeros(shape=(temlpLabel.__len__(), labelCount))
    labels = np_utils.to_categorical(temlpLabel)

    return  features, labels
'''
trainPath = '../dataset/pre224/people/train'
validationPath = '../dataset/pre224/people/validation'
#testPath = '../dataset/people/test'
day = '0426'
usolDlib = deep.usolDlib()

if os.path.isfile("trainXY" + day + ".npz"):
    tr, va, te = np.load('trainXY' + day +'.npz'), np.load('validationXY' + day+ '.npz'), np.load('testXY' + day + '.npz')
    trainFeatures, trainLabel = tr['x'], tr['y']
    validationFeatures, validationLabel = va['x'], va['y']
    #testFeatures, testLabel = va['x'], va['y']
else:
    trainFeatures, trainLabel = usolDlib.generateXYFromDir(path=trainPath)
    np.savez('trainXY' + day, x=trainFeatures, y=trainLabel)
    validationFeatures, validationLabel = usolDlib.generateXYFromDir(path=validationPath)
    np.savez('validationXY' + day, x=validationFeatures, y=validationLabel)
    #testFeatures, testLabel = usolDlib.generateXYFromDir(path=testPath)
    #np.savez('testXY' + day, x=testFeatures, y=testLabel)


#dlib.hit_enter_to_continue()
from keras import models
from keras import layers
from keras import optimizers
from keras.models import load_model
from keras.preprocessing.image import load_img
import matplotlib.pyplot as plt
from PIL import Image
import numpy
from usol import deep

idx2label = usolUtil.makeIndexToLabelFromDir(trainPath)
classCount = len(idx2label)
if os.path.isfile('dilb_based_model' + day + '.h5') == False:
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_dim=128))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(classCount, activation='softmax'))
    model.summary()

    model.compile(optimizer=optimizers.RMSprop(lr=2e-4),
                  loss='categorical_crossentropy',
                  metrics=['acc'])

    history = model.fit(trainFeatures,
                        trainLabel,
                        epochs=60,
                        batch_size=20,
                        validation_data=(validationFeatures, validationLabel))

    score = model.evaluate(trainFeatures, trainLabel, batch_size = 20)
    print("-----------------result!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------")
    print("%s  :   %2f%%" %(model.metrics_names[1], score[1]*100))

    print("-----------------model save!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------")
    model.save('dilb_based_model' + day + '.h5')

myModel = load_model('dilb_based_model' + day + '.h5')

testFile = '{}/{}/{}'.format(validationPath, 'parknare', '000065.jpg')
original = load_img(testFile)
plt.imshow(original)

img = Image.open(testFile).convert('RGB')
img = numpy.array(img)
dets = usolDlib.detector(img, 1)
testF = usolDlib.extractFeatureFromImg(dets=dets, img=img)

predictions = myModel.predict_classes(testF[0].reshape(1, -1))
prob = myModel.predict(testF[0].reshape(1, -1))
print(idx2label[predictions[0]])
print(np.amax(prob[0]))

from sklearn.neighbors import KNeighborsClassifier

knn =None
if os.path.isfile('knn_model' + day + '.pkl'):
    with open('knn_model' + day + '.pkl', 'rb') as f:
        knn = pickle.load(f)
else:
    print("-----------------knn fit & save!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------")
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(trainFeatures, trainLabel)
    model_score = knn.score(trainFeatures, trainLabel)
    print(model_score)
    with open('knn_model' + day + '.pkl', 'wb') as f:
        pickle.dump(knn, f)

print("-----------------knn predict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------")
result =  knn.predict(testF[0].reshape(1, -1))
print(idx2label[np.where(result[0]==1)[0][0]])
print('Finish training...')

print("--------------L2 distance!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!--------------")
i = 0
for  f in validationFeatures:
    if((validationLabel[i] == result[0]).all()):
        faceDistance = np.linalg.norm(testF[0] - f, axis=None, ord=2)
        if(faceDistance < 0.6):
            print(i)
            print(faceDistance)
            print(idx2label[np.where(validationLabel[i]==1)[0][0]])
    i = i +1

plt.show()