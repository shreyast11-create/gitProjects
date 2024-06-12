# importing libraries

import cv2 as cv
import sys
import numpy as np

# attempting to read the image as grayscale
gray_img = cv.imread(cv.samples.findFile("datasets/dog.jpg"), cv.IMREAD_GRAYSCALE)

# closing if image not found
if gray_img is None:
    sys.exit("Unable to read image")

# displaying image and adding 'forever-wait' until user presses a button
# cv.imshow("Gray Scale Dog", img)
# cv.waitKey(0)

# getting image negative
neg_img = cv.bitwise_not(gray_img)
# cv.imshow("Inverted Gray Scale Dog", neg_img)
# cv.waitKey(0)

# setting kernel size and blurring
blur_img = cv.blur(neg_img, (41, 11))
# cv.imshow("Blurred Negative Dog", blur_img)
# cv.waitKey(0)

# dividing gray scale image by blurred negative image to obtain 'pencil-like' features
pencil_img = cv.divide(gray_img, 255-blur_img, scale=256)
cv.imshow("Pencil Sketch Dog", pencil_img)
cv.waitKey(0)
