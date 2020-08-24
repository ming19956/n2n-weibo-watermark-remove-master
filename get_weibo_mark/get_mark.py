import cv2
import numpy as np

#图像减法 - 血液流动
ori1 = cv2.imread('../dataset/try/IMG_9359.JPG', cv2.IMREAD_UNCHANGED)
ori1 = cv2.cvtColor(ori1,cv2.COLOR_RGB2GRAY)
ori2 = cv2.imread('IMG_9360.JPG', cv2.IMREAD_UNCHANGED)
ori2 = cv2.cvtColor(ori2,cv2.COLOR_RGB2GRAY)


city3 = ori2 - ori1
# for i in city3:
#     for j in i:
#         if 0 <= j <= 5:
#             city3[i][j] = 255


city3[128 >= city3] = 0

ori2[140 >= ori2] = 0
city4 = ori2
city3 = ori2
#cv2.imshow('test_new', city4)



s = np.shape(city3)
print(s)
file = open("moin_moin_symbol_dong——test.txt", "w")
for i in range(760,s[0] - 8):
    for j in range(633,s[1] - 130):
        #if tmp[i][j][0] >= 250 and tmp[i][j][0] < 255:
        if ori2[i][j] == 0:
            file.write(str(ori2[i][j]))
            file.write("   ")
        elif 0 < ori2[i][j] <= 99:
            file.write(str(ori2[i][j]))
            file.write("  ")
        else:
            file.write(str(ori2[i][j]))
            file.write(" ")
    file.write("\n")

cv2.cvtColor(city3, cv2.COLOR_GRAY2BGRA)

cv2.imwrite("white_mark.png", city3)
tmp = cv2.imread("white_mark.png", cv2.IMREAD_UNCHANGED)
tmp = cv2.cvtColor(tmp, cv2.COLOR_GRAY2BGRA)

for each in range(s[0]):
    for each_each in range(s[1]):
        if tmp[each][each_each][0] < 150:
            tmp[each][each_each] = [0, 0, 0, 0]
#tmp[np.all(tmp[:][:][2] < 250)] = [0, 0, 0, 0]
s = np.shape(tmp)
print(s)
file = open("moin.txt", "w")
for i in range(767,s[0]-8):
    for j in range(633,s[1] - 111):
        #if tmp[i][j][0] >= 250 and tmp[i][j][0] < 255:
        if tmp[i][j][0] == 0:
            file.write(str(tmp[i][j][0]))
            file.write("   ")
        elif tmp[i][j][0] > 0 and tmp[i][j][0] <= 99:
            file.write(str(tmp[i][j][0]))
            file.write("  ")
        else:
            file.write(str(tmp[i][j][0]))
            file.write(" ")
    file.write("\n")

file_1 = open("moin_1.txt", "w")
for i in range(767,s[0]):
    for j in range(633,s[1]):
        #if tmp[i][j][0] >= 250 and tmp[i][j][0] < 255:
        if tmp[i][j][1] == 0:
            file_1.write(str(tmp[i][j][1]))
            file_1.write("   ")
        elif tmp[i][j][1] > 0 and tmp[i][j][1] <= 99:
            file_1.write(str(tmp[i][j][1]))
            file_1.write("  ")
        else:
            file_1.write(str(tmp[i][j][1]))
            file_1.write(" ")
    file_1.write("\n")

file_2 = open("moin_2.txt", "w")
for i in range(767,s[0]-8):
    for j in range(633,s[1] - 111):
        #if tmp[i][j][0] >= 250 and tmp[i][j][0] < 255:
        if tmp[i][j][2] == 0:
            file_2.write(str(tmp[i][j][2]))
            file_2.write("   ")
        elif tmp[i][j][2] > 0 and tmp[i][j][2] <= 99:
            file_2.write(str(tmp[i][j][2]))
            file_2.write("  ")
        else:
            file_2.write(str(tmp[i][j][2]))
            file_2.write(" ")

    file_2.write("\n")


cv2.imwrite("white_mark_fin.png", tmp)
cv2.imshow('city',ori2)
cv2.waitKey()

