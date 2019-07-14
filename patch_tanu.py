from PIL import Image, ImageOps
import os
import sys
import random
import time
import shutil
import argparse
import convert_tanu as cvt
# import skimage.io as io

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--random', help='ランダムでパンツが選ばれます', action='store_true')
parser.add_argument('-a', '--all', help='全てのパンツを変換します', action='store_true')
parser.add_argument('-i', '--input', help='ベースとなるテクスチャを指定できます', type=str, default='body_tanu.png')
parser.add_argument('-o', '--output', help='変換後の名前を指定できます', type=str, default='patched_tanu.png')
parser.add_argument('-p', '--pantie', help='変換するパンツの番号を数値で指定できます', type=int, default=-1)
args = parser.parse_args()

panties = os.listdir('./dream/')

if args.random:
    num = random.randint(0, len(panties))
    fname = panties[num]

if args.all:
    fdir = './converted/tanu/'
    os.makedirs(fdir, exist_ok=True)
    exists = len(os.listdir(fdir))
    panties = panties[exists:]
else:
    if args.random:
        num = random.randint(0, len(panties))
        fname = panties[num]
    else:
        if args.pantie is -1:
            fname = input("Type pantie name: ./dream/")
        else:
            fname = panties[args.pantie - 1]
    print('Process:' + fname)
    if fname in panties:
        panties = []
        panties.append(fname)
    else:
        print("Cannot find it")
        exit()

for fname in panties:
    pantie = cvt.convert2tanu(fname, fwrite=False)
    pantie = Image.fromarray(pantie)
    origin = Image.open(args.input)

    origin.paste(pantie, (55, 35), pantie)
    origin_transparent = Image.new("RGBA", (origin.size))
    origin_transparent.paste(pantie, (55, 35), pantie)
    origin_transparent.save('patched_transparent.png')

    origin.save(args.output)
    if args.all:
        print('Done ' + fname)
        origin_transparent.save(fdir + fname)
    else:
        print("Done. Please check {}.".format(args.output))
