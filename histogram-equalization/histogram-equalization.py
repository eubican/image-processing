"""
Created by eubican at 13.01.2022
Project: Histogram Equalization
"""
import sys
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def generate_histogram(image):
    histogram = np.zeros((256, 1))

    rows = image.shape[0]
    cols = image.shape[1]

    for i in range(rows):
        for j in range(cols):
            histogram[image[i, j]] += 1

    return histogram


def cumulative_distribution(histogram):
    tmp = np.zeros((256, 1))
    for i in range(256):
        tmp[i] = hist[i]

    cdf_array = np.zeros((256, 1))

    for i in range(1, 256):
        histogram[i] += histogram[i - 1]

    for i in range(256):
        cdf_array[i] = histogram[i]
        histogram[i] = tmp[i]

    cdf_array_min = np.min(cdf[np.nonzero(cdf)])
    cdf_array_max = np.max(cdf)

    return cdf_array, cdf_array_min, cdf_array_max


def equalize_histogram(cdf_array, cdf_array_min, image):
    equalized = np.zeros((256, 1))
    for i in range(256):
        equalized[i, 0] = round((cdf_array[i, 0] - cdf_array_min) / (image.size - cdf_array_min) * 255)

    return equalized


def create_enhanced_image(equalized, image):
    rows = image.shape[0]
    cols = image.shape[1]
    enhanced_img = np.zeros([rows, cols], np.uint8)
    for i in range(rows):
        for j in range(cols):
            enhanced_img[i, j] = equalized[image[i, j], 0]

    return enhanced_img


if __name__ == "__main__":
    img = cv.imread("resources/pic.png", 0)
    if img is None:
        print("Unable to load.")
        sys.exit(0)

    hist = generate_histogram(img)
    cdf, cdf_min, cdf_max = cumulative_distribution(hist)
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    equalized_image = equalize_histogram(cdf, cdf_min, img)
    enhanced_image = create_enhanced_image(equalized_image, img)

    # creating histograms of images
    fig, axs = plt.subplots(1, 2, constrained_layout=True, figsize=(12, 6))
    fig.suptitle('Image histograms', fontsize=16)

    axs[0].hist(img.flatten(), 256, [0, 256], color='r')
    axs[0].plot(cdf_normalized, color='b')
    axs[0].legend(('cdf', 'histogram'), loc='upper left')
    axs[0].set_title('Normal image')
    axs[0].set_xlabel('Pixel')
    axs[0].set_ylabel('Intensity')

    axs[1].hist(enhanced_image.flatten(), 256, [0, 256], color='r')
    axs[1].plot(cdf_normalized, color='b')
    axs[1].legend(('cdf', 'histogram'), loc='upper left')
    axs[1].set_title('Enhanced image')
    axs[1].set_xlabel('Pixel')
    axs[1].set_ylabel('Intensity')

    # save created figure
    plt.savefig('resources/outputs/histograms.png', dpi=300)

    # stacking images side-by-side
    res = np.hstack((img, enhanced_image))
    cv.imwrite('resources/outputs/result.png', res)
