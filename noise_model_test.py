import argparse
import string
import random
import numpy as np
import cv2
from PIL import Image
import  os
path = os.path.abspath("..")
if path == 'E:\yitiao':
    path = os.path.abspath(".")




#logo = ["mark_rewrite__Lucky_M.png", "mark_rewrite_aoi_bhinn.png", "mark_rewrite_BadTaste.png", "mark_rewrite_GO_Hank.png", "mark_rewrite_mamnunticha.png"]
#logo = ["mark_rewrite__Lucky_M.png"]
num_logo = 0
for r, dirs, files in os.walk(path + '/dataset/mark_logo_ran'):
    # Get all the images
    for file in files:
        num_logo += 1

def get_noise_model(noise_type="gaussian,0,50"):
    tokens = noise_type.split(sep=",")

    if tokens[0] == "gaussian":
        min_stddev = int(tokens[1])
        max_stddev = int(tokens[2])

        def gaussian_noise(img):
            noise_img = img.astype(np.float)
            stddev = np.random.uniform(min_stddev, max_stddev)
            noise = np.random.randn(*img.shape) * stddev
            noise_img += noise
            noise_img = np.clip(noise_img, 0, 255).astype(np.uint8)
            return noise_img
        return gaussian_noise
    elif tokens[0] == "clean":
        def add_text_clean(img):
            img = img.copy()
            #image = Image.fromarray(img)
            #image = image.resize((128, 128))
            return img
        return add_text_clean
        #return lambda img: img
    elif tokens[0] == "text":
        min_occupancy = int(tokens[1])
        max_occupancy = int(tokens[2])

        def add_text(img):
            img = img.copy()

            TRANSPARENCY = random.randint(88, 97)

            logo_ran = random.randint(2, num_logo)
            bigger = random.uniform(1, 2)

            image = Image.fromarray(img)
            path_mark = path + '/dataset/mark_logo_ran/mark_rewrite_{}.png'.format(logo_ran)

            watermark = Image.open(path_mark)
            hei = watermark.size[1]
            wid = watermark.size[0]

            watermark = watermark.resize((int(wid * bigger), int(hei * bigger)))

            hei = watermark.size[1]
            wid = watermark.size[0]

            if watermark.mode != 'RGBA':
                print("in if")
                alpha = Image.new('L', watermark.size, 255)
                watermark.putalpha(alpha)

            paste_mask = watermark.split()[3].point(lambda i: i * TRANSPARENCY / 100.)

            hei_i = image.size[1]
            wid_i = image.size[0]

            # random_W = random.randint(0, wid_i - wid)
            # random_H = random.randint(0, hei_i - hei)

            # image = image.resize((128,128))
            # image.paste(watermark, (128 - wid, 128 - hei), mask= paste_mask)

            # if hei_i < wid_i:
            #    image = image.resize((500, 375))
            #    image.paste(watermark, (500 - wid, 375 - hei), mask=paste_mask)
            # else:
            #    image = image.resize((375, 500))
            #    image.paste(watermark, (375 - hei, 500 - wid), mask=paste_mask)
            # print("size")
            # print(wid_i, hei_i)

            image.paste(watermark, (wid_i - wid, hei_i - hei), mask=paste_mask)
            # image.paste(watermark, (100 , 100 ), mask=paste_mask)
            # print(np.shape(image))
            # return img  #测试时请注释这一行 启用48行
            return image  # 训练模型时请注释这一行 启用47行

        return add_text
    elif tokens[0] == "impulse":
        min_occupancy = int(tokens[1])
        max_occupancy = int(tokens[2])

        def add_impulse_noise(img):
            occupancy = np.random.uniform(min_occupancy, max_occupancy)
            mask = np.random.binomial(size=img.shape, n=1, p=occupancy / 100)
            noise = np.random.randint(256, size=img.shape)
            img = img * (1 - mask) + noise * mask
            return img.astype(np.uint8)
        return add_impulse_noise
    else:
        raise ValueError("noise_type should be 'gaussian', 'clean', 'text', or 'impulse'")


def get_args():
    parser = argparse.ArgumentParser(description="test noise model",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image_size", type=int, default=256,
                        help="training patch size")
    parser.add_argument("--noise_model", type=str, default="gaussian,0,50",
                        help="noise model to be tested")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    image_size = args.image_size
    noise_model = get_noise_model(args.noise_model)

    while True:
        image = np.ones((image_size, image_size, 3), dtype=np.uint8) * 128
        noisy_image = noise_model(image)
        cv2.imshow("noise image", noisy_image)
        key = cv2.waitKey(-1)

        # "q": quit
        if key == 113:
            return 0


if __name__ == '__main__':
    main()