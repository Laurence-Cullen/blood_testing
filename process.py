import firebase_admin
import numpy as np
import numpy.ma as ma
from firebase_admin import credentials
from firebase_admin import firestore
from skimage import io
from skimage.filters import threshold_otsu
# import io

# # Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': 'ashra-blood',
# })
#
# db = firestore.client()

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


# def handle_test(request):
#     image = request.files.get('fileUpload', '')
#     name = request.form['studentName']
#
#     in_memory_file = io.BytesIO()
#     image.save(in_memory_file)
#     raw_image_data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
#
#     haem_conc = image_to_haemoglobin_grams_per_dl(raw_image_data)
#
#     doc_ref = db.collection(u'children').add({
#         u'name': name,
#         u'haemoglobin_g_per_dL': haem_conc,
#         u'school': u'St. Xavier’s Collegiate School'
#     })
#
#     return 'student is named: ' + name + ', got image:' + str(type(image))


if __name__ == '__main__':
    main()
