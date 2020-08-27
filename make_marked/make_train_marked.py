import cv2
import numpy as np
import os
import random
from PIL import Image
logo = []
for r, dirs, files in os.walk('../dataset/mark_logo_ran_new'):
    # Get all the images
    for file in files:
        img = cv2.imread(os.sep.join([r, file]), cv2.IMREAD_UNCHANGED)
        if img is not None:
            logo.append(img)
        else:
            print("%s not found."%(file))

images = []
for r, dirs, files in os.walk('../dataset/try'):
    # Get all the images
    for file in files:
        img = cv2.imread(os.sep.join([r, file]))
        if img is not None:
            images.append(img)
        else:
            print("%s not found."%(file))

num_logo = len(logo)
for i in range(len(images)):
    cur = random.randint(0, num_logo - 1)
    #hei = np.shape(logo[cur])[0]
    #wid = np.shape(logo[cur])[1]

    hei_i = np.shape(images[i])[0]
    wid_i = np.shape(images[i])[1]
    img = images[i].copy()

    TRANSPARENCY = random.randint(88, 97)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    watermark = Image.fromarray(logo[cur])
    s = np.shape(watermark)
    flag = random.uniform(1.45, 2)
    watermark = watermark.resize((int(s[1] / flag), int(s[0] / flag)), Image.ANTIALIAS)
    hei = watermark.size[1]
    wid = watermark.size[0]
    # print("mark_size")
    # print(hei)
    # print(wid)

    if watermark.mode != 'RGBA':
        print("in if")
        alpha = Image.new('L', watermark.size, 255)
        watermark.putalpha(alpha)


    paste_mask = watermark.split()[3].point(lambda i: i * TRANSPARENCY / 100.)

    hei_i = image.size[1]
    wid_i = image.size[0]

    image.paste(watermark, (wid_i - wid, hei_i - hei), mask=paste_mask)
    #image.paste(watermark, (100 , 100 ), mask=paste_mask)
    #image.paste(watermark, (wid_i - wid, hei_i - hei))

    image.save("../inputdir/{}.png".format(i+20))
#for i in range(len(images)):
#    hei = np.shape(logo[i // 800])[0]
#    wid = np.shape(logo[i // 800])[1]

#    hei_i = np.shape(images[i])[0]
#    wid_i = np.shape(images[i])[1]
    # print(hei_i, wid_i)
#    if hei_i >= wid_i:
#        images[i] = cv2.resize(images[i], (375, 500))
        # print(np.shape(images[i]))
        # print(images[i][500 - hei : 500, 375 - wid : 375])
#        for j in range(hei):
#            for k in range(wid):
#                if logo[i // 800][j, k][0] < 100:
#                    continue
#                images[i][500 - hei + j, 375 - wid + k] = logo[i // 800][j, k]
#    else:
#        images[i] = cv2.resize(images[i], (500, 375))
        # print(images[i][375 - hei : 375, 500 - wid : 500][0:3])
        # print(ori1[:, :][0:3])
#        for j in range(hei):
#            for k in range(wid):
#                if logo[i // 800][j, k][0] < 100:
#                    continue
#                images[i][375 - hei + j, 500 - wid + k] = logo[i // 800][j, k]
#    cv2.imwrite("../dataset/train/{}.png".format(i), images[i])
