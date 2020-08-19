import cv2
import numpy as np

img1 = cv2.imread("IMG_9359.JPG")
img2 = cv2.imread("../inputdir/IMG_9360.JPG")

dif = cv2.absdiff(img1, img2)

cv2.imwrite("tmp.png", dif)

tmp = cv2.imread("tmp.png", cv2.IMREAD_UNCHANGED)
tmp = cv2.cvtColor(tmp, cv2.COLOR_RGB2BGRA)
tmp[np.all(tmp == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
cv2.imwrite("weibo_mark.png", tmp)
#cv2.imwrite("res.png", img)
