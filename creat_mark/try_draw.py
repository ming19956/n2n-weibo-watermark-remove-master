import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import random
import time

def GBK2312():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)   # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str

## Make canvas and set the color

b,g,r,a = 0,255,0,0
j = 0
img_2 = np.zeros((30, 180, 3), np.uint8)
with open("moin_moin_symbol_dong.txt", "r") as d:
    for each in d.readlines():
        each = each.replace("   ", " ")
        i = 0
        for each in each.split(" "):
            if each == "\n" or each == "":
                continue
            img_2[j][i] = each
            i += 1
        j += 1

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()1234567890'
names = []

#names = ["_Lucky_M", "mamnunticha", "GO_Hank", "aoi_bhinn", "BadTaste"]
#names = ["@脸脸颐真的微博"]
## Use simsum.ttc to write Chinese.
j = 1
#names = [""]
while len(names) < 99:
    str = "@"
    ran_ch_en = random.randint(1,3)
    #ran_ch_en = 2
    for each in range(random.randint(4, 15)):
        if ran_ch_en == 1:
            str += random.choice(alphabet)
        elif ran_ch_en == 2:
            str += GBK2312()
        elif ran_ch_en == 3:
            str += random.choice(alphabet)
            str += GBK2312()
    if str not in names:
        names.append(str)
    else:
        continue

    j += 1
    fontpath = "./38.ttf"  # <== 这里是宋体路径
    #str = "@脸脸颐真的微博"
    img_pil = Image.fromarray(img_2)
    draw = ImageDraw.Draw(img_pil)
    if ran_ch_en == 2 or ran_ch_en == 3:
        font = ImageFont.truetype(fontpath, 22)
        draw.text((34, 0), str, font=font, fill=(255, 255, 255))
    else:
        font = ImageFont.truetype(fontpath, 23)
        draw.text((34, -4), str, font=font, fill=(255, 255, 255))

    img = np.array(img_pil)


    #s = (20, 100, 3)
    tmp = img
    s = np.shape(tmp)

    for each in range(1, s[0] - 1):
        for each_each in range(1, s[1] - 1):
            if tmp[each][each_each][0] < 60:
                #if tmp[each + 1][each_each] != 0 and tmp[each - 1][each_each] != 0:
                tmp[each][each_each] = [0, 0, 0]
            elif tmp[each][each_each][0] < 100 and tmp[each][each_each][0] != 0:
                res = random.randint(130, 150)
                tmp[each][each_each] = [res, res, res]
            elif tmp[each][each_each][0] < 150 and tmp[each][each_each][0] != 0:
                res = random.randint(170, 200)
                tmp[each][each_each] = [res, res, res]
            elif tmp[each][each_each][0] < 200 and tmp[each][each_each][0] != 0:
                res = random.randint(200, 255)
                tmp[each][each_each] = [res, res, res]
            while tmp[each][each_each][0] < tmp[each + 1][each_each][0] and tmp[each][each_each][0] < tmp[each - 1][each_each][0] and tmp[each][each_each][0] != 0:
                tmp[each][each_each] = tmp[each][each_each] + [1, 1, 1]


    # file = open("moin_new.txt", "w")
    # for i in range(s[0]):
    #     for j in range(s[1]):
    #         #if tmp[i][j][0] >= 250 and tmp[i][j][0] < 255:
    #         if tmp[i][j][0] <= 9:
    #             file.write(str(tmp[i][j][0]))
    #             file.write("   ")
    #         elif tmp[i][j][0] > 0 and tmp[i][j][0] <= 99:
    #             file.write(str(tmp[i][j][0]))
    #             file.write("  ")
    #         else:
    #             file.write(str(tmp[i][j][0]))
    #             file.write(" ")
    #     file.write("\n")


    ## Display
    #cv2.imshow("res", img);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imwrite("tmp.png", img)
    tmp = cv2.imread("tmp.png", cv2.IMREAD_UNCHANGED)
    tmp = cv2.cvtColor(tmp, cv2.COLOR_RGB2BGRA)
    tmp[np.all(tmp == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    cv2.imwrite("../dataset/mark_logo_ran_new/mark_rewrite_{}.png".format(j), tmp)
    #cv2.imwrite("../dataset/mark_logo_ran/mark_rewrite_{}.png".format(j), tmp)
    #cv2.imwrite("res.png", img)
