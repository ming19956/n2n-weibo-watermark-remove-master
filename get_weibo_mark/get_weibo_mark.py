import cv2
import numpy as np

img1 = cv2.imread("IMG_9412.JPG")
img2 = cv2.imread("IMG_9413.JPG")

dif = cv2.absdiff(img2, img1)

cv2.imshow("img", dif)
cv2.waitKey()
#dif = cv2.subtract(img2, img1)
cv2.imwrite("tmp.png", dif)

tmp = cv2.imread("tmp.png", cv2.IMREAD_UNCHANGED)
tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2BGRA)
tmp[np.all(tmp == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
cv2.imwrite("weibo_mark_new.png", tmp)
#cv2.imwrite("res.png", img)
