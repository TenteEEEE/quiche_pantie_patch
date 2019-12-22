import skimage.io as io
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np


def perspective_transform(img, matrix):
    homography = skt.ProjectiveTransform(matrix=matrix)
    out = skt.warp(img, homography)
    return out


def resize(img, mag):
    return skt.resize(img, (np.int(img.shape[0] * mag[0]), np.int(img.shape[1] * mag[1])), anti_aliasing=True, mode='reflect')


def affine_transform(img, mx, my, phix=0, phiy=0, divx=2, divy=2, inv=False):
    [r, c, d] = img.shape
    src_cols = np.linspace(0, c, 10)
    src_rows = np.linspace(0, r, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    shifter_row = np.zeros(src.shape[0])
    shifter_col = np.zeros(src.shape[0])
    if inv:
        linex = np.linspace(np.pi + phix, np.pi / divx + phix, src.shape[0])
        liney = np.linspace(np.pi + phiy, np.pi / divy + phiy, src.shape[0])
    else:
        linex = np.linspace(np.pi / divx + phix, np.pi + phix, src.shape[0])
        liney = np.linspace(np.pi / divy + phiy, np.pi + phiy, src.shape[0])
    shifter_row = -(np.sin(linex) * mx)
    shifter_col = -(np.sin(liney) * my)
    dst_rows = src[:, 1] + shifter_row
    dst_cols = src[:, 0] + shifter_col
    dst = np.vstack([dst_cols, dst_rows]).T
    affin = skt.PiecewiseAffineTransform()
    affin.estimate(src, dst)
    return skt.warp(img, affin)


def affine_transform_by_arr(img, arrx, arry, smoothx=False, smoothy=False, mvx=10, mvy=10):
    [r, c, d] = img.shape
    src_cols = np.linspace(0, c, int(np.sqrt(len(arrx))))
    src_rows = np.linspace(0, r, int(np.sqrt(len(arry))))
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    if smoothx:
        lx = len(arrx)
        arrx = np.convolve(arrx, np.ones(mvx) / mvx, mode='valid')
        arrx = skt.resize(arrx, (lx, 1), anti_aliasing=True, mode='reflect')[:, 0]
    if smoothy:
        ly = len(arry)
        arry = np.convolve(arry, np.ones(mvy) / mvy, mode='valid')
        arry = skt.resize(arry, (ly, 1), anti_aliasing=True, mode='reflect')[:, 0]
    dst_rows = src[:, 1] + arrx
    dst_cols = src[:, 0] + arry
    dst = np.vstack([dst_cols, dst_rows]).T
    affin = skt.PiecewiseAffineTransform()
    affin.estimate(src, dst)
    return skt.warp(img, affin)


def ribbon_inpaint(image):
    mask = io.imread('./mask/ribbon4inpaint.png')
    ribbon = image[19:58, 5:35, :3]
    ribbon_mask = (mask[19:58, 5:35, 1] > 0)[:, :, None]
    removed = ribbon * (mask[19:58, 5:35, 1] < 1)[:, :, None].astype(np.float)
    search_area = image[60:100 - 1, :40, :3].astype(np.float)
    [r, c, d] = ribbon_mask.shape
    dx = search_area.shape[1] - ribbon.shape[1]
    score = np.zeros(dx)
    for x in range(dx):
        inpainter = search_area[:, x:x + c, :] * ribbon_mask
        inpainted = removed + inpainter
        for vx in range(dx):
            score[x] += np.mean((inpainted - search_area[:, vx:vx + c])**2)
    optimum = np.argmin(score)
    inpainter = search_area[:, optimum:optimum + c, :] * ribbon_mask
    inpainted = removed + inpainter
    image[19:58, 5:35, :3] = np.uint8(inpainted)
    return image


def alpha_brend(img1, img2, mask):
    return img1 * mask[:, :, None] + img2 * (1 - mask)[:, :, None]
