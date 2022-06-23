from skimage.morphology import disk, binary_erosion
from cropper.segmentation import binarize
import numpy as np
import math

from matplotlib import pyplot as plt
from skimage import io


def get_edges(mask: np.ndarray) -> np.ndarray:
    '''
    Extracts edges with a width of one pixel from binary mask

    @param: mask
       binary array obtand after binarization of image

    @returns
        binary arry with edges
    '''
    edges = mask ^ binary_erosion(mask, footprint=disk(1, bool))
    return edges


def is_corner(i: int, j: int, mask: np.ndarray, size=50) -> bool:
    '''
    Determines whether a given pixel can be a corner pixel

        We are working with mask which is binary array. All the input pixels are
    the border piexels of segmentation. These pixels belong to the sides of 
    segmented rectangles or to the rectangle's corners.
        This method checks the environment around given pixel and sums all the values.
    If pixel belongs to the side then percent of TRUE values in it's environment is more
    than 40%. If this percent is less then this pixel is more probable to be a corner
    pixel

    @param: i
        y-coordinate of given pixel
    @param: j
        x-coordinate of given pixel
    @param: mask
        binary array (segmentation mask) obtained after binarization
    @param: size
        size of the environment to check

    @returns:
        True if given pixel is probable to be corner
    '''
    
    environment = mask[(i-size):(i+(size+1)), (j-size):(j+(size+1))]
    occupancy_rate = environment.sum() / (environment.shape[0] * environment.shape[1])
    
    if occupancy_rate < 0.4:
        return True

    return False


def choose_corners(points: np.ndarray, h: int, w: int) -> np.ndarray:
    '''
    Extracts 4 pixels from "corners" list as corners of the document.
    Pixels are arranged in special order:
        1) upper left
        2) upper right
        3) lower right
        4) lower left
    This order is needed for following cropping transformation

    @param: corners
        list of pixels' coordinates
    @param: h
        hight of processed image in pixels
    @param: w
        width of processed image in pixels

    @returns
        list with 4 values coordinates of determened corners
    '''

    def closest_point(x0: int, y0: int):
        '''
        Finds closest point to the given corner

        @param x0:
            x-coordinate of the given corner
        @param y0:
            y-coordinate of the given corner
        '''
        min_distance = np.inf
        closest_point = None

        for x1, y1 in points:
            distance = math.hypot(x1 - x0, y1 - y0)
            if distance < min_distance:
                min_distance = distance
                closest_point = [x1, y1]

        return closest_point

    corners = []
    corners.append(closest_point(0, 0))
    corners.append(closest_point(w, 0))
    corners.append(closest_point(w, h))
    corners.append(closest_point(0, h))

    return np.array(corners)


def detect_corners(mask: np.ndarray, pad_width: int=50) -> np.ndarray:
    '''
    Detects corners of the document on given segmentation mask

    @param: mask
        binary array - segmentation mask obtained
        after applying binarize() method

    @param: pad_width
        width of the applied padding    

    @returns
        list of 4 corners coordinates
        they are arranged in special order:
            1) upper left
            2) upper right
            3) lower right
            4) lower left
        this order is needed for the following cropping transformation
    '''
    # Mask must be padded for the proper detection
    # In cases when document is located on the edge of the image
    # get_edges() method works incorrect
    mask = np.pad(mask, pad_width, constant_values=False)

    edges = get_edges(mask)
    corners = []
    # Detect pixels that are the most probable to be corners
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i][j] and is_corner(i, j, mask, size=pad_width):
                corners.append([j, i])

    corners = np.array(corners)
    # Select pixels considered as corners
    corners = choose_corners(corners, edges.shape[0], edges.shape[1])
    corners = np.array([[x - pad_width, y - pad_width] for x, y in corners])

    return corners




if __name__ == '__main__':
    image = io.imread('./docs/example.jpg')
    mask = binarize(image)
    edges = get_edges(mask)
    corners = detect_corners(mask)

    fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    plt.gray()
    axes[0].imshow(image)
    axes[0].set_title('Original')

    axes[1].imshow(mask)
    axes[1].set_title('Mask')
            
    axes[2].imshow(edges)
    axes[2].set_title('Edges')

    for x, y in corners:
        axes[2].scatter(x, y, s=150, color='r')

    for a in axes.ravel():
        a.axis('off')

    plt.show()
    plt.close(fig)