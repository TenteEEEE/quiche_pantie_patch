import skimage.transform as skt
import skimage.morphology as skm
import numpy as np

def perspective_transform(img,matrix):
    homography = skt.ProjectiveTransform(matrix=matrix)
    out = skt.warp(img,homography)
    return out

def resize(img,mag):
    return skt.resize(img,(np.int(img.shape[0]*mag[0]),np.int(img.shape[1]*mag[1])),anti_aliasing=True,mode='reflect')

def affine_transform(img,mx,my,inv=False):
    [r,c,d] = img.shape
    src_cols = np.linspace(0, c, 10)
    src_rows = np.linspace(0, r, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    shifter_row = np.zeros(src.shape[0])
    shifter_col = np.zeros(src.shape[0])
    if inv:
        line = np.linspace(np.pi, np.pi/2, src.shape[0])
    else:
        line = np.linspace(np.pi/2, np.pi, src.shape[0])
    shifter_row = -(np.sin(line)*mx)
    shifter_col = -(np.sin(line)*my)
    dst_rows = src[:, 1] + shifter_row
    dst_cols = src[:, 0] + shifter_col
    dst = np.vstack([dst_cols, dst_rows]).T
    affin = skt.PiecewiseAffineTransform()
    affin.estimate(src,dst)
    return skt.warp(img, affin)
