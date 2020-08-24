import tensorflow as tf
import numpy as np
import cv2
import os
path = os.path.abspath("..")

def _tf_fspecial_gauss(size, sigma=1.5):
    """Function to mimic the 'fspecial' gaussian MATLAB function"""
    x_data, y_data = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]

    x_data = np.expand_dims(x_data, axis=-1)
    x_data = np.expand_dims(x_data, axis=-1)

    y_data = np.expand_dims(y_data, axis=-1)
    y_data = np.expand_dims(y_data, axis=-1)

    x = tf.constant(x_data, dtype=tf.float32)
    y = tf.constant(y_data, dtype=tf.float32)

    g = tf.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    return g / tf.reduce_sum(g)


def SSIM(img1, img2, k1=0.01, k2=0.02, L=1, window_size=11):
    """
    The function is to calculate the ssim score
    """

    img1 = tf.expand_dims(img1, 0)
    img1 = tf.expand_dims(img1, -1)
    img2 = tf.expand_dims(img2, 0)
    img2 = tf.expand_dims(img2, -1)

    window = _tf_fspecial_gauss(window_size)

    mu1 = tf.nn.conv2d(img1, window, strides = [1, 1, 1, 1], padding = 'VALID')
    mu2 = tf.nn.conv2d(img2, window, strides = [1, 1, 1, 1], padding = 'VALID')

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = tf.nn.conv2d(img1*img1, window, strides = [1 ,1, 1, 1], padding = 'VALID') - mu1_sq
    sigma2_sq = tf.nn.conv2d(img2*img2, window, strides = [1, 1, 1, 1], padding = 'VALID') - mu2_sq
    sigma1_2 = tf.nn.conv2d(img1*img2, window, strides = [1, 1, 1, 1], padding = 'VALID') - mu1_mu2

    c1 = (k1*L)**2
    c2 = (k2*L)**2

    ssim_map = ((2*mu1_mu2 + c1)*(2*sigma1_2 + c2)) / ((mu1_sq + mu2_sq + c1)*(sigma1_sq + sigma2_sq + c2))

    return tf.reduce_mean(ssim_map)

def tf_log10(x):
    numerator = tf.log(x)
    denominator = tf.log(tf.constant(10, dtype=numerator.dtype))
    return numerator / denominator

def PSNR(y_true, y_pred):
    max_pixel = 255.0
    return 10.0 * tf_log10((max_pixel ** 2) / (tf.reduce_mean(tf.square(y_pred - y_true))))

def get_diff(path1, path2):
    image1 = []
    image2 = []
    for r, dirs, files in os.walk(path1):
        # Get all the images
        for file in files:
            image1.append(file)

    for r, dirs, files in os.walk(path2):
        # Get all the images
        for file in files:
            image2.append(file)
    average1 = 0
    average2 = 0
    for i in range(len(image1)):
        img1 = cv2.imread("{}/{}".format(path1,image1[i]))
        img2 = cv2.imread("{}/{}".format(path2,image2[i]))


        h1 = np.shape(img1)[0]
        w1 = np.shape(img1)[1]

        h2 = np.shape(img2)[0]
        w2 = np.shape(img2)[1]

        img1 = img1[h1 - 60: h1, w1 - 180: w1]
        img2 = img2[h2 - 60: h2, w2 - 180: w2]

        img1 = np.array(img1.astype('float32'))
        img2 = np.array(img2.astype('float32'))
        img1 = tf.constant(img1)
        img2 = tf.constant(img2)

        _SSIM_ = tf.image.ssim(img1, img2, 1.0)
        _PSNR_ = tf.image.psnr(img1, img2, 255.0)

        rgb1 = tf.unstack(img1, axis=2)
        r1 = rgb1[0]
        g1 = rgb1[1]
        b1 = rgb1[2]

        rgb2 = tf.unstack(img2, axis=2)
        r2 = rgb2[0]
        g2 = rgb2[1]
        b2 = rgb2[2]

        ssim_r = SSIM(r1, r2)
        ssim_g = SSIM(g1, g2)
        ssim_b = SSIM(b1, b2)

        ssim = tf.reduce_mean(ssim_r + ssim_g + ssim_b) / 3
        psnr = PSNR(img1, img2)

        with tf.Session() as sess:
            #print("{} image diff".format(i))
            #print(sess.run(_SSIM_))
            #print(sess.run(ssim))
            average1 += sess.run(_SSIM_)
            average2 += sess.run(ssim)
    file = open('{}/text_noise/compare_result.txt'.format(path), "a")
    print("average")
    print(average1 / len(image1))
    print(average2 / len(image1))
    file.write("average : {}  |  {}".format(average1 / len(image1), average2 / len(image1)))
    file.write("\n")

if __name__ == '__main__':
    get_diff("../input_best_model", "../outputdir")
    #img1 = np.array(imageio.imread('../inputdir/0.png', pilmode='RGB').astype('float32'))
    #img2 = np.array(imageio.imread('../outputdir/0.png', pilmode='RGB').astype('float32'))
    #img1 = cv2.imread('../inputdir/0.png')
    #img2 = cv2.imread('../outputdir_cont/0.png')

    #h1 = np.shape(img1)[0]
    #w1 = np.shape(img1)[1]

    #h2 = np.shape(img2)[0]
    #w2 = np.shape(img2)[1]

    #img1 = img1[h1 - 60: h1, w1 - 180 : w1]
    #img2 = img2[h2 - 60: h2, w2 - 180 : w2]


    #img1 = np.array(img1.astype('float32'))
    #img2 = np.array(img2.astype('float32'))
    #img1 = tf.constant(img1)
    #img2 = tf.constant(img2)

    #_SSIM_ = tf.image.ssim(img1, img2, 1.0)
    #_PSNR_ = tf.image.psnr(img1, img2, 255.0)

    #rgb1 = tf.unstack(img1, axis=2)
    #r1 = rgb1[0]
    #g1 = rgb1[1]
    #b1 = rgb1[2]

    #rgb2 = tf.unstack(img2, axis=2)
    #r2 = rgb2[0]
    #g2 = rgb2[1]
    #b2 = rgb2[2]

    #ssim_r=SSIM(r1,r2)
    #ssim_g=SSIM(g1,g2)
    #ssim_b=SSIM(b1,b2)

    #ssim = tf.reduce_mean(ssim_r+ssim_g+ssim_b)/3
    #psnr = PSNR(img1, img2)


    #with tf.Session() as sess:
    #    print(sess.run(_SSIM_))
    #    print(sess.run(_PSNR_))
    #    print(sess.run(ssim))
    #    print(sess.run(psnr))