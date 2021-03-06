from skimage.filters import threshold_local, gaussian, rank, threshold_minimum
from skimage.morphology import disk, binary_closing
from skimage import color, measure
from skimage.util import img_as_ubyte
from scipy.ndimage import binary_fill_holes
from scipy.fftpack import dct, idct
import numpy as np

from matplotlib import pyplot as plt
from skimage import io


def rgb_to_bgr(img: np.ndarray) -> np.ndarray:
    '''Converts rgb image to gray scalar

    Args:
        img: image read using skimage.io.imread() or
            similar method
    
    Returns:
        image converted to monochrome format
    '''
    gray = color.rgb2gray(img)
    frequencies = dct(dct(gray, axis=0), axis=1)
    frequencies[:2,:2] = 0
    gray = idct(idct(frequencies, axis=1), axis=0)
    gray = (gray - gray.min()) / (gray.max() - gray.min())

    return gray


def preprocess(img: np.ndarray) -> np.ndarray:
    '''Converts rgb image to gray scalar and applies Gauss
    filter for bluring

    Args:
        img: image read using skimage.io.imread() or
            similar method
    
    Returns:
        blurred image converted to monochrome format
    '''
    gray = rgb_to_bgr(img)
    gray = gaussian(gray, 2)

    return gray


def get_biggest_region(mask: np.ndarray) -> np.ndarray:
    '''Finds the biggest connected white region and lives only it.
    This group will be initial mask of the document

    Args:
        mask: binary array obtained after binarization of original image

    Returns:
        mask  without white noise from background
    '''
    mask = measure.label(mask)
    mask = (mask == 1 + np.argmax([r.filled_area for r in measure.regionprops(mask)]))

    return mask


def apply_binary_closing(mask: np.ndarray, size_1: int=10, size_2: int=5) -> np.ndarray:
    '''Two different methods for binary holes closing are used.
    They are needed to remove holes obtained by text on the receipts.

    Args:
        mask: mask obtained after applying thresholding function
        size_1: size of the disk for binary_closing() from skimage
        size_2: size of the disk for binaary_fill_holes() from scipy

    Returns:
        final binarization mask
    '''
    mask = binary_closing(mask, footprint=disk(size_1, bool))
    mask = binary_fill_holes(mask, structure=disk(size_2, bool))

    return mask


def post_processing(mask: np.ndarray) -> np.ndarray:
    '''Applies post processing methods after thersholding binarization

    Args:
        mask: mask obtained after thersholding function

    Returns:
        final binarization mask
    '''
    mask = get_biggest_region(mask)
    mask = apply_binary_closing(mask)

    return mask


def otsu_binarization(gray: np.ndarray, disc_size: int=8) -> np.ndarray:
    '''Thresholding function
    Applies Otsu binarization to preprocessed image

    Args:
        gray: preprocess image in gray scalar with applied Gaus filter
        disc_size: size of the environment to check in otsu() method

    Returns:
        binary array (mask)
    '''
    gray = img_as_ubyte(gray)
    local_otsu = rank.otsu(gray, disk(disc_size))
    mask = gray >= local_otsu

    return mask


def local_binarization(gray: np.ndarray, block_size: int=101, offset: int=0) -> np.ndarray:
    '''Thresholding function
    Applies Local binarization to preprocessed image

    Args:
        gray: preprocess image in gray scalar with applied Gaus filter
        block_size: size of the environment to check in local() method

    Returns:
        binary array (mask)
    '''
    local = threshold_local(gray, block_size=block_size, offset=offset)
    mask = gray > local

    return mask


def minimum_binarization(gray: np.ndarray) -> np.ndarray:
    '''Thresholding function
    Applies minimum binarization to preprocessed image

    Args:
        gray: preprocess image in gray scalar with applied Gaus filter

    Returns:
        binary array (mask)
    '''
    thresh_min = threshold_minimum(gray)
    mask = gray > thresh_min

    return mask


def binarize(img: np.ndarray) -> np.ndarray:
    '''Binarizes given image

    Args:
        img: given rgb image

    Returns:
        binary array (segmentation mask)
    '''    
    gray = preprocess(img)
    # Otsu binarization showed the best results on tests
    # You can try another thesholding functions here
    mask = otsu_binarization(gray)
    mask = post_processing(mask)

    return mask




def demonstration():
    '''Demonstrates work of methods from this file'''
    image = io.imread('./docs/example.jpg')
    gray = rgb_to_bgr(image)
    gauss = preprocess(image)
    otsu = otsu_binarization(gauss)
    receipt = get_biggest_region(otsu)
    mask = apply_binary_closing(receipt)

    fig, axes = plt.subplots(1, 6, figsize=(20, 6))
    fig.canvas.manager.set_window_title('Segmentation') 
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
    axes[5].set_title('Final mask')

    for a in axes.ravel():
        a.axis('off')
    
    plt.show()
    plt.close(fig)