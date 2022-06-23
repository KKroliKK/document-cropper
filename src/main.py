from cropper import crop_image
from cropper import crop_image_pipeline
from skimage import io


crop_image('./docs/example.jpg', './docs/example_cropped.jpg')
crop_image_pipeline('./docs/example.jpg', './docs/example_pipeline.jpg')