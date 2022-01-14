"""
Created by eubican at 14.01.2022
Project: 
"""
import numpy as np
import cv2 as cv
import sys


def flip_image(image, flag):
    rows = image.shape[0]
    cols = image.shape[1]
    flipped = np.zeros([rows, cols], np.uint8)

    # to indicate whether the image will be flipped vertical(0)/horizontal(1)

    if flag == 0:
        for i in range(rows):
            flipped[i, :] = image[rows - i - 1, :]
    elif flag == 1:
        for j in range(cols):
            flipped[:, j] = image[:, cols - j - 1]

    return flipped


if __name__ == "__main__":
    img = cv.imread("resources/iroh.jpg")
    if img is None:
        print("Unable to load.")
        sys.exit(0)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite("resources/outputs/grayscale.png", gray)

    vertical_flipped = flip_image(gray, 0)
    cv.imwrite("resources/outputs/vertical_flipped.png", vertical_flipped)

    horizontal_flipped = flip_image(gray, 1)
    cv.imwrite("resources/outputs/h_flipped.png", horizontal_flipped)
