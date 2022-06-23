from imageCropper import crop_image
from skimage import io


image = io.imread('example.jpg')
cropped = crop_image(image)
io.imsave('example_cropped.jpg', cropped)