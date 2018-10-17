import os
import dlib
import  numpy
import cv2
from  PIL import Image

oriPath = '../dataset/images_0409'
destPath = '../dataset/pre_over_100/people/testConfidence/'
predictor_path = 'shape_predictor_68_face_landmarks.dat'
shapePredictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()
size = 224, 224

dirs = os.listdir(oriPath)
j = 10
for dir in dirs:
    files = os.listdir(oriPath + '/' + dir)
    i = 1
    for file in files:
        filePath = oriPath + '/' + dir + '/' + file
        img = Image.open(filePath).convert('RGB')
        npy_img = numpy.array(img)
        dets = detector(npy_img, 1)

        if not os.path.exists(destPath + dir):
            os.makedirs(destPath + dir)

        if len(dets) == 1:
            for k, d in enumerate(dets):
                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    k, d.left(), d.top(), d.right(), d.bottom()))
                img = img.crop((d.left(), d.top(), d.right(), d.bottom()))
                if 100 < img.size[0]:
                    img.save(destPath + '/' + dir + '/' + str(j) + str(i) + '.jpg')
                '''
                new_img = Image.new("RGB", (224, 224), "white")  # 바탕 이미지 생성

                if 224 < img.size[0] or 224 < img.size[1]:
                    img.thumbnail(size, Image.ANTIALIAS)

                i_offset = int(round((224 - img.size[0]) / 2))
                j_offset = int(round((224 - img.size[1]) / 2))
                area = (i_offset, j_offset, img.size[0] + i_offset, img.size[1] + j_offset)
                new_img.paste(img, area)

                new_img.save(destPath + '/' + dir + '/' + str(i) + '.jpg')
                '''
                i = i + 1
    j = j + 1