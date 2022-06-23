from cropper.imageCropper import crop_image
from skimage import io
import warnings

warnings.filterwarnings("ignore")

image = io.imread('./docs/example.jpg')
cropped = crop_image(image)
io.imsave('./docs/example_cropped.jpg', cropped)

# import os
# print(os.path.dirname(os.path.realpath(__file__)))
# print(__file__)