from ctu import reader, display
from scipy import ndimage
import skimage
import numpy as np

def BodyMask(img, threshold=-400):
    img_shape = img.shape
    img = ndimage.zoom(img, 256/np.asarray(img.shape), order=0)
    bodymask = img > threshold
    bodymask = ndimage.binary_closing(bodymask)
    bodymask = ndimage.binary_fill_holes(bodymask, structure=np.ones((3, 3))).astype(int)
    bodymask = ndimage.binary_erosion(bodymask, iterations=1)
    bodymask = skimage.measure.label(bodymask.astype(int), connectivity=1)
    regions = skimage.measure.regionprops(bodymask.astype(int))
    if len(regions) > 0:
        max_region = np.argmax(list(map(lambda x: x.area, regions))) + 1
        bodymask = bodymask == max_region
        bodymask = ndimage.binary_dilation(bodymask, iterations=1)
    real_scaling = np.asarray(img_shape)/256
    logical_mask = ndimage.zoom(bodymask, real_scaling, order=0)
    return logical_mask.astype(int)
