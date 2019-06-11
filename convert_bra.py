import os
import sys
import skimage.io as io
import skimage.transform as skt
import skimage.morphology as skm
from skimage.color import rgb2hsv, hsv2rgb
import numpy as np
import matplotlib.pyplot as plt

panties = os.listdir('./dream/')
bra_mask = io.imread('./mask/bra.png')[:430, 1024:1024 + 620, :]
bra_center = io.imread('./mask/bra_center.png')[:430, 1024:1024 + 620, :]
bra_shade = io.imread('./material/bra_shade.png')[:430, 1024:1024 + 620, :]
[r, c, d] = bra_mask.shape

for fname in panties:
    print('Process: ' + fname)
    pantie = io.imread('./dream/' + fname)

    # center painting
    center_texture = pantie[20:180, -130:]
    center_texture = skt.resize(center_texture, (np.int(center_texture.shape[0] * 1.6), np.int(center_texture.shape[1] * 1.6)), anti_aliasing=True, mode='reflect')
    [hr, hc, hd] = center_texture.shape
    posx = 20
    posy = 170
    padx = c - hc - posx
    pady = r - hr - posy
    center_texture = (np.pad(center_texture, [(posy, pady), (posx, padx), (0, 0)], mode='constant'))
    center_texture[:, :, 3] = bra_center[:, :, 0] / 255.0

    # base color painting
    front = pantie[20:100, 30:80, :]
    base = np.mean(np.mean(front, axis=0), axis=0) / 255.0
    if np.mean(base[:3]) < 0.4:  # median estimation provides better estimation for dark panties
        base = np.median(np.median(front, axis=0), axis=0) / 255.0
    base = base[:3]
    base_texture = np.copy(bra_mask).astype(np.float32) / 255.0
    base_texture[:, :, :3] = (base_texture[:, :, :3] * base)

    # convined them and shading
    center_mask = (bra_center[:, :, 0][:, :, None] / 255.0).astype(np.float32)
    convined_texture = base_texture * (1 - center_mask) + center_texture * center_mask
    shade = rgb2hsv(np.tile((bra_shade[:, :, 3].astype(np.float32) / 255.0)[:, :, None], [1, 1, 3]) * base)
    np.mean(shade[:, :, 0])
    if np.mean(shade[:, :, 0]) < 0.01:
        shade[:, :, 0] += 1.5
    else:
        shade[:, :, 0] -= 1
    shade[:, :, 1] *= 3 * np.mean(base)
    shade[:, :, 2] /= 1 + 0.5 * np.mean(base)
    shade = hsv2rgb(shade)
    convined_texture[:, :, :3] -= shade
    convined_texture[:, :, 3] = (bra_mask[:, :, 0] / 255.0).astype(np.float32)
    convined_texture = np.clip(convined_texture, 0.0, 1.0)

    # finalize
    convined_texture = (convined_texture * 255.0).astype(np.uint8)
    # plt.imshow(convined_texture)
    io.imsave('./converted/bra/'+fname, convined_texture)
