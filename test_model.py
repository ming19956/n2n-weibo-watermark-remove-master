import argparse
import numpy as np
from pathlib import Path
import cv2
from model import get_model
from noise_model_test import get_noise_model
import os
path = os.path.abspath("..")
if path == 'E:\yitiao':
    path = os.path.abspath(".")

def get_args():
    parser = argparse.ArgumentParser(description="Test trained model",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image_dir", type=str, required=True,
                        help="test image dir")
    parser.add_argument("--model", type=str, default="srresnet",
                        help="model architecture ('srresnet' or 'unet')")
    parser.add_argument("--weight_file", type=str, required=True,
                        help="trained weight file")
    parser.add_argument("--test_noise_model", type=str, default= "clean",
                        help="noise model for test images")
    parser.add_argument("--output_dir", type=str, default=None,
                        help="if set, save resulting images otherwise show result using imshow")
    args = parser.parse_args()
    return args


def get_image(image):
    image = np.clip(image, 0, 255)
    return image.astype(dtype=np.uint8)


def main():
    args = get_args()
    image_dir = path + "/" + args.image_dir
    weight_file = args.weight_file

    val_noise_model = get_noise_model(args.test_noise_model)
    model = get_model(args.model)
    model.load_weights(weight_file)

    if args.output_dir:

        output_dir = Path(path + "/" + args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(Path(image_dir).glob("*.*"))

    for image_path in image_paths:

        image = cv2.imread(str(image_path))

        #image = image[:(h // 16) * 16, :(w // 16) * 16]  # for stride (maximum 16)
        h, w, _ = image.shape
        if h * w > 172800 * 8:
            flag = np.sqrt(h * w / 172800 / 8)
            h = int (h / flag)
            w = int (w / flag)

        out_image = np.zeros((h, w * 1, 3), dtype=np.uint8)
        noise_image = val_noise_model(image)
        s = np.shape(noise_image)
        if s[0] * s[1] > 172800 * 8:
            flag = np.sqrt(s[0] * s[1] / 172800 / 8)
            noise_image = cv2.resize(noise_image, (int(s[1] / flag), int(s[0] / flag)))
        pred = model.predict(np.expand_dims(noise_image, 0))
        denoised_image = get_image(pred[0])
        out_image[:, :w] = denoised_image
        if args.output_dir:
            output_dir.joinpath("/")

            cv2.imwrite(str(output_dir.joinpath(image_path.name))[:-4] + ".png", out_image)
        else:
            cv2.imshow("result", out_image)
            key = cv2.waitKey(-1)
            # "q": quit
            if key == 113:
                return 0
    path1 = path + '/compare_diff/compare_diff.py'                     # 测试时注释此两行
    init = path + '/val_image/init'
    os.system("python %s --init_path %s --output_path %s" % (path1, init, output_dir))      # 寻找最优模型时，取消注释

if __name__ == '__main__':
    main()