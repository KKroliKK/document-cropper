from cropper import crop_image, crop_image_pipeline
from cropper import segmentation, cornerDetection, imageCropper, cropperPipeline


crop_image('./docs/example.jpg', './docs/example_cropped.jpg')
crop_image_pipeline('./docs/example.jpg', './docs/example_pipeline.jpg')


# segmentation.demonstration()
# cornerDetection.demonstration()
# imageCropper.demonstration()
# cropperPipeline.demonstration()