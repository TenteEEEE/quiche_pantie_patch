from PIL import Image, ImageOps
import os
import sys
import numpy as np
import argparse
import warnings

parser = argparse.ArgumentParser(description='Fourier transformer for the panties')
parser.add_argument("--rgb", action="store_true", help='Enable Full-Color Fourier transform (Default:Gray-scale)')
parser.add_argument("--long", action="store_true", help='Enable 16bit PNG (Gray-scale mode only)')
args = parser.parse_args()

panties = sorted(os.listdir('./dream/'))
os.makedirs('./converted/Fourier/', exist_ok=True)
if args.rgb:
    mode = 'RGB'
    if args.long:
        warnings.warn('In RGB mode, it cannot apply 16bit mode')
else:
    mode = 'L'
for fname in panties:
    print('Process: ' + fname + ', Mode:' + mode)
    pantie = Image.open('./dream/' + fname).convert(mode)
    img = np.array(pantie).astype(np.float64)/255.0
    fimg = np.log(np.abs(np.fft.fftshift(np.fft.ifft2(img, axes=(0, 1)))))
    fmin = np.min(fimg)
    fimg -= fmin
    fmax = np.max(fimg)
    fimg /= fmax
    if args.long and not args.rgb:
        fpantie = Image.fromarray(np.uint16(fimg * 65535))
    else:
        fpantie = Image.fromarray(np.uint8(fimg * 255))
    fpantie.save('./converted/Fourier/' + fname[:-4] + '_' + str(fmin)[0:7] + '_' + str(fmax)[0:6] + '.png')
print("Done. Please check patched.png.")
