from PIL import Image, ImageOps
import os
import sys
import argparse
import warnings


def norm_img(img):
    img -= np.min(img)
    return img / np.max(img)


parser = argparse.ArgumentParser(description='Phase retrieval for the Fourier transfromed panties')
parser.add_argument("--hio", action="store_true", help='Apply Hybrid-input-output algorithm (Default: Error Reduction Algorithm)')
parser.add_argument("--itr", type=int, default=100, help='Number of iteration (Default:100)')
parser.add_argument("--beta", type=float, default=0.9, help='Ratio of influence in HIO algorithm [Recommended: 0.5~1.0] (Default:0.9)')
parser.add_argument("--gpu",  action="store_true", help='Enable GPU processing [required:cupy] (Default:False)')
args = parser.parse_args()

if args.gpu:
    print('GPU processing mode is enabled')
    import cupy as np
else:
    import numpy as np

fpanties = os.listdir('./converted/Fourier/')
os.makedirs('./converted/Fourier_inv/', exist_ok=True)
# fpanties = fpanties[len(os.listdir('./converted/Fourier_inv/')):]
for fname in fpanties:
    strs = fname.split('_')
    pantie = strs[0] + '.png'
    fmin = np.float64(strs[1])
    fmax = np.float64(strs[2][:-4])
    print('Process: ' + pantie)

    fpantie = Image.open('./converted/Fourier/' + fname)
    fimg_origin = np.fft.ifftshift(np.exp(np.array(fpantie,dtype=np.float64) / np.max(np.array(fpantie)) * fmax + fmin))
    mask = (np.array(Image.open('./dream/' + pantie))[:, :, 3] > 0).astype(np.float32)[:, :, None]
    [r, c, d] = fimg_origin.shape
    img = np.fft.ifft2(fimg_origin * np.exp(2j * np.pi * np.random.rand(r, c, d)), axes=(0, 1))  # Initialize the phase
    if args.hio:
        mask_inv = 1 - mask
        previous_img = np.copy(img)
    for i in range(args.itr):
        if args.hio:
            fimg = np.fft.fft2((np.abs(img) * mask + (np.abs(previous_img) - args.beta * np.abs(img)) * mask_inv) * np.exp(1j * np.angle(img)), axes=(0, 1))
            previous_img = np.copy(img)
        else:  # Error reduction
            fimg = np.fft.fft2(np.abs(img) * mask * np.exp(1j * np.angle(img)), axes=(0, 1))
        img = np.fft.ifft2(fimg_origin * np.exp(1j * np.angle(fimg)), axes=(0, 1))
    if np.max(np.array(fpantie)) == 255:
        img = (norm_img(np.abs(img)) * 255).astype(np.uint8)
    else:
        img = (norm_img(np.abs(img)) * 65535).astype(np.uint16)
    if args.gpu:
        img = np.asnumpy(img)
    if args.hio:
        outname = './converted/Fourier_inv/' + pantie[:-4] + '_hio.png'
    else:
        outname = './converted/Fourier_inv/' + pantie
    restored_pantie = Image.fromarray(img)
    restored_pantie.save(outname)
