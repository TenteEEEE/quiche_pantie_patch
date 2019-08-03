import os
import sys
import skimage.io as io
import skimage.transform as skt
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.filters import gaussian
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Pantie2Bra Converter')
parser.add_argument("--num", type=int, default=0, help='Set the pantie number. When you set with --all, it is the start number [Default: Latest]')
parser.add_argument("--all", action="store_true", help='Process the all panties [Default: False]')
parser.add_argument("--pad", action="store_true", help='Enable transparent padding [Default: Disable]')
parser.add_argument("--lace", action="store_true", default=False, help='Enable lace bra mode [Default: Frill]')
parser.add_argument("--disable_ribbon", action="store_true", default=False, help='Disable the center ribbon paint [Default: Enable]')
parser.add_argument("--disable_decoration", action="store_true", default=False, help='Disable the decoration such as frill and lace [Default: Enable]')
parser.add_argument("--disable_shading", action="store_true", default=False, help='Disable the automatic shading [Default: Enable]')
parser.add_argument("--disable_texture", action="store_true", default=False, help='Disable the automatic base texture painting [Default: Enable]')
args = parser.parse_args()
os.makedirs('converted', exist_ok=True)

panties = sorted(os.listdir('./dream/'))
ribbon_mask = io.imread('./mask/ribbon.png')
bra_mask = io.imread('./mask/bra.png')[:430, 1024:1024 + 620, :]
bra_center = io.imread('./mask/bra_center.png')[:430, 1024:1024 + 620, :]
bra_shade = io.imread('./material/bra_shade.png')[:430, 1024 - 620:1024 + 620, :]
frill = io.imread('./material/bra_frill.png')[:430, 1024 - 620:1024 + 620, :]
lace = io.imread('./material/bra_lace.png')[:430, 1024 - 620:1024 + 620, :]
[r, c, d] = bra_mask.shape
os.makedirs('./converted/bra/', exist_ok=True)


def alpha_brend(ref, template):
    return ref * (1 - template[:, :, -1][:, :, None]) + template[:, :, :3] * template[:, :, -1][:, :, None]


if args.all:
    panties = panties[args.num - 1:]
else:
    panties = list([panties[args.num - 1]])

for fname in panties:
    pantie = io.imread('./dream/' + fname)
    print('Process: ' + fname)

    # crop center texture
    center_texture = pantie[20:140, -170:-15]
    center_texture = skt.resize(center_texture, (np.int(center_texture.shape[0] * 1.6), np.int(center_texture.shape[1] * 1.6)), anti_aliasing=True, mode='reflect')
    [hr, hc, hd] = center_texture.shape

    # make seamless design
    design = rgb2gray(center_texture[:, :, :3])[::-1, ::-1]
    design = (design - np.min(design)) / (np.max(design) - np.min(design))
    edge = 30
    design_seamless = gaussian(design, sigma=3)
    design_seamless[edge:-edge, edge:-edge] = design[edge:-edge, edge:-edge]
    y = np.arange(-hr / 2, hr / 2, dtype=np.int16)
    x = np.arange(-hc / 2, hc / 2, dtype=np.int16)
    design_seamless = (design_seamless[y, :])[:, x]  # rearrange pixels
    design_seamless = np.tile(design_seamless, (3, 3))

    # paste center texture
    posx = 20
    posy = 230
    padx = c - hc - posx
    pady = r - hr - posy
    center_texture = (np.pad(center_texture, [(posy, pady), (posx, padx), (0, 0)], mode='constant'))
    center_texture[:, :, 3] = bra_center[:, :, 0] / 255.0

    # base color painting and shading seamless design
    front = pantie[20:100, 30:80, :]
    front_shade = pantie[100:150, 0:40, :]
    base = np.mean(np.mean(front, axis=0), axis=0) / 255.0
    if np.mean(base[:3]) < 0.4:  # median estimation provides better estimation for dark panties
        base = np.median(np.median(front, axis=0), axis=0) / 255.0
    base = base[:3]
    base_shade = (np.median(np.median(front, axis=0), axis=0) / 255.0)[:3]
    base_texture = np.copy(bra_mask).astype(np.float32) / 255.0
    base_texture[:, :, :3] = (base_texture[:, :, :3] * base)
    if args.disable_texture is False:
        shade = rgb2hsv(np.tile((design_seamless)[:, :, None], [1, 1, 3]) * base_shade)
        shade[:, :, 0] -= 0
        shade[:, :, 1] *= -4 + (1 - np.mean(base)) * 6
        shade[:, :, 2] /= 6 + 3 * np.mean(base)
        shade = hsv2rgb(shade)
        base_texture[:, :, :3] -= shade[:r, :c, ]

    # convine center and base textures and shading
    center_mask = (bra_center[:, :, 0][:, :, None] / 255.0).astype(np.float32)
    convined_texture = base_texture * (1 - center_mask) + center_texture * center_mask
    convined_texture = np.concatenate([convined_texture[:, ::-1, :], convined_texture], axis=1)
    if args.disable_shading is False:
        shade = rgb2hsv(np.tile((bra_shade[:, :, 3].astype(np.float32) / 255.0)[:, :, None], [1, 1, 3]) * base_shade)
        shade[:, :, 0] -= 1
        shade[:, :, 1] *= 0.5 + np.mean(base) / 3
        shade[:, :, 2] /= 1 + 1 * np.mean(base)
        shade = hsv2rgb(shade)
        convined_texture[:, :, :3] -= shade

    # Paste frill or lace
    if args.disable_decoration is False:
        if args.lace:
            decoration = np.copy(lace).astype(np.float32) / 255.0
        else:
            decoration = np.copy(frill).astype(np.float32) / 255.0
        deco_shade = np.median(pantie[5, :, :3], axis=0) / 255.0
        shade = rgb2hsv(decoration[:, :, :3] * deco_shade)
        shade[:, :, 1] *= 0.5 + np.mean(base) / 3
        decoration_shaded = hsv2rgb(shade)
        decoration_shaded = np.dstack((decoration_shaded, decoration[:, :, 3]))
        convined_texture[:, :, :3] = alpha_brend(convined_texture[:, :, :3], decoration_shaded)

    # Crop ribbon and pasete <0070.png
    if args.disable_ribbon is False:
        ribbon = np.copy(pantie)
        ribbon[:, :, 3] = ribbon_mask[:, :, 1]
        ribbon = ribbon[19:58, 8:30] / 255.0
        ribbon_bi = np.concatenate([ribbon[:, ::-1, :], ribbon], axis=1)
        rib_r = 383
        rib_c = base_texture.shape[1] - int(ribbon_bi.shape[1] / 2)
        convined_texture[rib_r:rib_r + ribbon_bi.shape[0], rib_c:rib_c + ribbon_bi.shape[1], :3] = \
            alpha_brend(convined_texture[rib_r:rib_r + ribbon_bi.shape[0], rib_c:rib_c + ribbon_bi.shape[1], :3], ribbon_bi)

    # finalize
    final_mask = np.copy(bra_mask[:, :, 0]).astype(np.float32) / 255
    if args.disable_ribbon is False:
        final_mask[rib_r:rib_r + ribbon.shape[0], :ribbon.shape[1]] += ribbon[:, :, 3]
    final_mask = np.concatenate([final_mask[:, ::-1], final_mask], axis=1)
    if args.disable_decoration is False:
        final_mask += decoration[:, :, 3]
    final_mask = np.clip(final_mask, 0, 1)
    convined_texture[:, :, 3] = final_mask
    convined_texture = np.clip(convined_texture, 0.0, 1.0)
    convined_texture = (convined_texture * 255.0).astype(np.uint8)

    if args.pad:
        padx = int((2048 - convined_texture.shape[1]) / 2)
        pady = 2048 - 430
        print(padx)
        print(pady)
        io.imsave('./converted/bra/' + fname, np.pad(convined_texture,[(0, pady), (padx,padx), (0, 0)], mode='constant'))
    else:
        io.imsave('./converted/bra/' + fname, convined_texture)
