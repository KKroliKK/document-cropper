import segmentation
from cropper import *
import numpy as np

from skimage import io
from matplotlib import pyplot as plt


image = io.imread('./docs/example.jpg')
gray = segmentation.rgb_to_bgr(image)
gauss = segmentation.preprocess(image)
otsu = segmentation.otsu_binarization(gauss)
receipt = segmentation.get_biggest_region(otsu)
mask = segmentation.apply_binary_closing(receipt)

p_mask = np.pad(mask, pad_width=50, constant_values=False)

edges = cornerDetection.get_edges(p_mask)
corners = cornerDetection.detect_corners(mask)

cropped = imageCropper.crop_image(image)

fig, axes = plt.subplots(2, 5, figsize=(20, 10))
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

plt.show()
plt.close(fig)