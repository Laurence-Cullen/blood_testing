import numpy as np
import numpy.ma as ma
from skimage import io

from skimage.filters import threshold_otsu


# map from blood image red band pixel values to a
# haemoglobin concentration in grams per deci litre
color_to_haemoglobin_conc = {
    14: 128,
    12: 144,
    10: 168,
    8: 189,
    6: 198,
    4: 220
}


def red_value_to_haemoglobin_conc(red_value):
    best_match = None
    minimum_diff = 255

    for value in color_to_haemoglobin_conc:
        absolute_diff = abs(red_value - color_to_haemoglobin_conc[value])
        if absolute_diff < minimum_diff:
            best_match = value
            minimum_diff = absolute_diff

    return best_match


def image_to_haemoglobin_grams_per_dl(image):
    red_band = image[:, :, 0]
    green_band = image[:, :, 1]

    thresh = threshold_otsu(green_band)
    mask = green_band < thresh
    masked_red_band = ma.masked_array(red_band, mask)
    mean_red_value = np.mean(masked_red_band)

    return red_value_to_haemoglobin_conc(mean_red_value)


def main():
    image = io.imread('blood_circle.jpg')

    conc = image_to_haemoglobin_grams_per_dl(image)
    print(conc, 'grams per dL')


if __name__ == '__main__':
    main()
