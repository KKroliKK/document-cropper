from cropper.imageCropper import crop_image
from cropper.cropperPipeline import crop_image_pipeline
from skimage import io
import warnings

warnings.filterwarnings("ignore")

image = io.imread('./docs/example.jpg')

cropped = crop_image(image)
io.imsave('./docs/example_cropped.jpg', cropped)

crop_image_pipeline(image, './docs/example_pipeline.jpg')