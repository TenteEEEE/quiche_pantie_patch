import skimage.transform as skt
import skimage.morphology as skm
import numpy as np

def perspective_transform(img,matrix):
    homography = skt.ProjectiveTransform(matrix=matrix)
    out = skt.warp(img,homography)
    return out

def resize(img,mag):
    return skt.resize(img,(np.int(img.shape[0]*mag[0]),np.int(img.shape[1]*mag[1])),anti_aliasing=True,mode='reflect')
