from skimage.transform import ProjectiveTransform, warp
from scipy.spatial import distance
from skimage.util import img_as_ubyte
from cropper.cornerDetection import detect_corners
from cropper.segmentation import binarize
import numpy as np

from skimage import io
from matplotlib import pyplot as plt


def crop_image(filename: str=None, new_filename: str=None, image: np.ndarray=None) -> np.ndarray:
    '''Cropes document from given image

    Args:
        filename: path to the image to crop;
            if value is None method expects to have not None image parameter
        new_filename: if is not None saves cropped file in specified directory
        image: imgae to crop in form of np.ndarray
    
    Returns:
        cropped image in form of ndarray
    '''
    if filename is not None:
        image = io.imread(filename)
    mask = binarize(image)
    corners = detect_corners(mask)

    d = distance.pdist(corners)
    w = int(max(d[0], d[5]))
    h = int(max(d[2], d[3]))

    tr = ProjectiveTransform()
    tr.estimate(np.array([[0,0], [w,0], [w,h], [0,h]]), corners)

    cropped = warp(image, tr, output_shape=(h, w), order=1, mode="reflect")

    cropped = img_as_ubyte(cropped)

    if new_filename is not None:
        io.imsave(new_filename, cropped)
    return cropped




def demonstration():
    '''Demonstrates work of cropping method from this file'''
    image = io.imread('./docs/example.jpg')
    mask = binarize(image)
    corners = detect_corners(mask)
    cropped = crop_image(image=image)

    fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    fig.canvas.manager.set_window_title('Image Cropping')
    plt.gray()
    axes[0].imshow(image)
    axes[0].set_title('Original')

    axes[1].imshow(mask)
    axes[1].set_title('Corners')
            
    axes[2].imshow(cropped)
    axes[2].set_title('Cropped')

    for x, y in corners:
        axes[1].scatter(x, y, s=150, color='r')

    for a in axes.ravel():
        a.axis('off')

    plt.show()
    plt.close(fig)