# -*- encoding: cp949 -*-
import datetime
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import numpy as np
import pickle
from keras.models import load_model
from usol import usolUtil
from usol.deep import usolDlib
from keras_vggface.vggface import VGGFace
from PIL import Image
import UsolDeepCore

usolDlib = usolDlib()
myModel = load_model('hs_model.h5')
with open('knn_model_resnet50vgg_max_0511.pkl', 'rb') as f:
    knn = pickle.load(f)
'''
vgg_conv = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(224, 224, 3))
vgg_conv.summary()
'''
resnet_vgg = VGGFace(model='resnet50', include_top=False,
                    input_shape=(224, 224, 3), pooling=None, weights='vggface')
resnet_vgg.summary()


test = np.load('testXY_resnet50vgg_max_0511.npz')
testFeatures, testLabel = test['x'], test['y']
#idx2label = usolUtil.makeIndexToLabelFromDir('../dataset/pre/people/validation')
with open('hs_model_label.pkl', 'rb') as f:
    idx2label = pickle.load(f)
print(idx2label)

class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print('new connection')
        self.write_message("Ready server.")
        WSHandler.clients.append(self)

    def on_message(self, message):
        #print('message received %s' % message)
        print('message received')
        #test = UsolDeepCore.facePridict(message)
        recImg = usolUtil.bas64ToRGB(message)
        dets = usolDlib.detector(np.array(recImg), 1)
        print("Number of faces detected: {}".format(len(dets)))

        if len(dets)  > 0 & len(dets)  < 4:
            # Now process each face we found.
            #features = usolDlib.extractFeatureFromImg(dets=dets, img=imgData)
            features = []
            for k, d in enumerate(dets):
                img = recImg.crop((d.left(), d.top(), d.right(), d.bottom()))
                img = img.resize((224, 224), Image.ANTIALIAS)
                #img.show()
                npImg = np.array(img)
                npImg = npImg.reshape(1,224,224,3)
                feature =resnet_vgg.predict(npImg)
                #normalization. because training feature coverted normalization
                feature = (feature - feature.min()) / feature.max() - feature.min()
                features.append(feature)

            print("-----------------dnn predict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------")
            for f in features:
                predictions = myModel.predict_classes(f.reshape(1, -1))
                prob = myModel.predict(f.reshape(1, -1))
                dnnPridict = "unknown"
                if (np.amax(prob[0]) > 0.9):
                    dnnPridict = idx2label[predictions[0]]

                print(idx2label[predictions[0]])
                print(np.amax(prob[0]))
                self.write_message("dnn predict @@" + dnnPridict)
                self.write_message("dnn detail(" + idx2label[predictions[0]]  + " / " + "dnn score(" + str(np.amax(prob[0])) + ")")
            print("-----------------knn predict!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------")
            knnPridict = "unknown"
            for f in features:
                result = knn.predict(f.reshape(1, -1))
                if(1 in result[0]):
                    print( idx2label[np.where(result[0] == 1)[0][0]])
                    knnPridict = idx2label[np.where(result[0] == 1)[0][0]]
                    print("--------------L2 distance!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!--------------")
                    i = 0
                    l2dists = []
                    for vf in testFeatures:
                        #if ((testLabel[i] == result[0]).all()):
                        temp = f.reshape(-1)
                        dist =np.linalg.norm(f.reshape(-1) - vf , axis=None, ord=None)
                        l2dists.append(dist)

                    l2dists = np.array(l2dists)
                    print("L2 distance(max " + str(np.max(l2dists)) + " / min " + str(np.min(l2dists)) + ")")
                    self.write_message("knn predict @@" + knnPridict + ")")
                    self.write_message("L2 distance(max " + str(np.max(l2dists)) + " / min " + str(np.min(l2dists))  + ")")
                else:
                    print("Knn No result")
                    self.write_message("Knn No result")
        elif len(dets)  >  3 :
            self.write_message("found too many faces")
        else:
            self.write_message("can't find a face")

    def on_close(self):
        print('connection closed')
        WSHandler.clients.remove(self)

    @classmethod
    def write_to_clients(cls):
        print("Writing to clients")
        for client in cls.clients:
            client.write_message("Hi there!")

if __name__ == "__main__":
    application = tornado.web.Application(handlers=[(r"/ws", WSHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9984)
    #tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=15))
    tornado.ioloop.IOLoop.instance().start()