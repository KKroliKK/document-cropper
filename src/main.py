from document_cropper import crop_image, crop_image_pipeline
from document_cropper import segmentation, corner_detection, image_cropper, cropper_pipeline


crop_image('./docs/example.jpg', './docs/example_cropped.jpg')
crop_image_pipeline('./docs/example.jpg', './docs/example_pipeline.jpg')
crop_image_pipeline('./docs/example.jpg')

# segmentation.demonstration()
# corner_detection.demonstration()
# image_cropper.demonstration()
# cropper_pipeline.demonstration()