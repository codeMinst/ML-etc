#얼굴 추출모델을 트레이닝 시키기 위해 데이터셋의 전처리 및 얼굴 위치값을 저장하기 위한 코드
import os
import dlib
import  numpy
from PIL import Image
from  shutil import  copyfile
import shutil

path = '../dataset/people/train/ts'
predictor_path = 'shape_predictor_68_face_landmarks.dat'
shapePredictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()
size = 224, 224

dirs = os.listdir(path)
for dir in dirs:
    files = os.listdir(path + '/' + dir)
    fw = open('dataset/collection_face_pos/val/' + dir + '.txt', 'w')
    i = 1
    for file in files:
        filePath = path + '/' + dir + '/' + file
        print(filePath)

        new_img = Image.new("RGB", (224, 224), "white")
        img = Image.open(filePath).convert('RGB')

        if 224 < img.size[0] or 224 < img.size[1]:
            img.thumbnail(size, Image.ANTIALIAS)

        i_offset = int(round((224 - img.size[0]) / 2))
        j_offset = int(round((224 - img.size[1]) / 2))
        area = (i_offset, j_offset, img.size[0] + i_offset, img.size[1]  + j_offset)
        new_img.paste(img, area)

        npy_img = numpy.array(new_img)
        dets = detector(npy_img, 1)

        if len(dets) == 1:
            for k, d in enumerate(dets):
                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    k, d.left(), d.top(), d.right(), d.bottom()))

                src = path + '/' + dir + '/' + file
                dst = 'dataset/collection/val/' + dir + '/' + dir + '_' + str(i).zfill(4) + '.jpg'
                fw.write(str(i).zfill(4) + " {} {} {} {}\n".format(d.left(), d.top(), d.right(), d.bottom()))

                if not os.path.exists('dataset/collection/val/' + dir):
                    os.makedirs('dataset/collection/val/' + dir)
                new_img.save(dst)
                #copyfile(src, dst)
                i = i + 1
    fw.close()