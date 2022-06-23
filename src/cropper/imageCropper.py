from skimage.transform import ProjectiveTransform, warp
from scipy.spatial import distance
from cropper.cornerDetection import detect_corners
from cropper.segmentation import binarize
import numpy as np

from skimage import io
from matplotlib import pyplot as plt
from os import walk
from tqdm import tqdm


def crop_image(image: np.ndarray) -> np.ndarray:
    '''
    Cropes document from given rgb image
    '''
    # Get segmentation mask of the initial image
    mask = binarize(image)

    # Find corners of the document
    #   Corners are returned in special order:
    #       1) upper left and then clockwise
    corners = detect_corners(mask)

    # Compute width and hight of the resulting cropped
    # document
    d = distance.pdist(corners)
    w = int(max(d[0], d[5]))
    h = int(max(d[2], d[3]))

    tr = ProjectiveTransform()
    tr.estimate(np.array([[0,0], [w,0], [w,h], [0,h]]), corners)

    cropped = warp(image, tr, output_shape=(h, w), order=1, mode="reflect")

    return cropped




if __name__ == '__main__':
    # directory = './example_images/'
    directory = './images/'
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend(filenames)
        files.sort()
        break


    for filename in tqdm(files[2:3]):
        image = io.imread(directory + filename)
        mask = binarize(image)
        corners = detect_corners(mask)
        cropped = crop_image(image)

        fig, axes = plt.subplots(1, 3, figsize=(20, 10))
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
        # plt.savefig('./crop_res/' + filename)

        plt.close(fig)