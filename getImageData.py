import os
import dlib
from skimage import io
import cv2
from  PIL import Image

# 가져올 파일들이 있는 directory path
path_dir = 'vgg_face2/test/n000259'
save_dir = 'dataset/people/test/n000259'
file_list = os.listdir(path_dir)        # path 에 존재하는 파일 목록 가져오기
img_list = []

for file in file_list:
    img_list.append(cv2.imread(path_dir + '/' + file, cv2.IMREAD_COLOR))
    print("Processing file: {}".format(file))

detector = dlib.get_frontal_face_detector()
win = dlib.image_window()

i = 0
for  img in img_list:
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    # face detect
    for j, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            j, d.left(), d.top(), d.right(), d.bottom()))

    win.clear_overlay()
    win.set_image(img)
    win.add_overlay(dets)

    img_trim = img[d.top():d.bottom(), d.left():d.right()]
    cv2.imwrite(save_dir  + '/' + file_list[i], img_trim)
    i = i + 1


#dlib.hit_enter_to_continue()




'''
if (len(sys.argv[1:]) > 0):
    #img = io.imread(sys.argv[1])
    dets, scores, idx = detector.run(img, 1, -1)
    for i, d in enumerate(dets):
        print("Detection {}, score: {}, face_type:{}".format(
            d, scores[i], idx[i]))
'''

'''
f = open(path_dir  + "/" + file_list[0], 'r')
faceInfo = []

i = 0
while True:
    line = f.readline()
    faceInfo.append(line)
    if not line:
        break
    print(line)
    i = i + 1

f.close()
'''