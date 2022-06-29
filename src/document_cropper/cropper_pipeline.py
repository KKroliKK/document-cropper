from document_cropper import corner_detection, image_cropper, segmentation
from matplotlib import pyplot as plt
from skimage import io
import numpy as np


def crop_image_pipeline(filename: str=None, new_filename: str=None, image: np.ndarray=None):
    '''Cropes document from given image and shows all the processing stages

    Args:
        filename: path to the image to crop (.jpg or .png)
            if value is None method expects to have not None image parameter
        new_filename: if is not None saves cropped file in specified directory
            else shows the result with plt.show() method
        image: image to crop in form of np.ndarray
    '''
    if filename is not None:
        image = io.imread(filename)

    gray = segmentation.rgb_to_bgr(image)
    gauss = segmentation.preprocess(image)
    otsu = segmentation.otsu_binarization(gauss)
    receipt = segmentation.get_biggest_region(otsu)
    mask = segmentation.apply_binary_closing(receipt)

    p_mask = np.pad(mask, pad_width=50, constant_values=False)

    edges = corner_detection.get_edges(p_mask, edge_width=6)
    corners = corner_detection.detect_corners(mask)

    cropped = image_cropper.crop_image(image=image)

    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    fig.canvas.manager.set_window_title('Whole Pipeline')
    axes = axes.ravel()
    plt.gray()

    axes[0].imshow(image)
    axes[0].set_title('Original')

    axes[1].imshow(gray)
    axes[1].set_title('Gray')

    axes[2].imshow(gauss)
    axes[2].set_title('Gauss filter')

    axes[3].imshow(otsu)
    axes[3].set_title('Otsu Thresholding')

    axes[4].imshow(receipt)
    axes[4].set_title('Extracted receipt')

    axes[5].imshow(mask)
    axes[5].set_title('Segmentation mask')

    axes[6].imshow(p_mask)
    axes[6].set_title('Padded mask')

    axes[7].imshow(edges)
    axes[7].set_title('Edges')

    axes[8].imshow(image)
    axes[8].set_title('Corners')

    axes[9].imshow(cropped)
    axes[9].set_title('Cropped')

    for x, y in corners:
        axes[8].scatter(x, y, s=150, color='r')

    for a in axes:
        a.axis('off')

    if new_filename is None:
        plt.show()
    else:
        plt.savefig(new_filename)

    plt.close(fig)


def demonstration():
    '''Demonstrates work of pipeline'''
    crop_image_pipeline('./docs/example.jpg')