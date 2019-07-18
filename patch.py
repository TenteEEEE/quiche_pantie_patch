import os
import sys
import numpy as np
import argparse
import importlib
from src.image_loader import *
sys.path.append('./src/')
import models

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', help='Choose your model', choices=models.namelist)
parser.add_argument('-a', '--all', help='If you set pantie number, it will be start number and works with force overwriting',  action='store_true')
parser.add_argument('-f', '--force', help='Overwrite the patched textures even if it exists',  action='store_true')
parser.add_argument('-i', '--input', help='Name of the base texture', type=str)
parser.add_argument('-o', '--output', help='Name of the patched texture', type=str, default='patched.png')
parser.add_argument('-p', '--pantie', help='Choose pantie number', type=int, default=0)
parser.add_argument('-t', '--transparent', help='Make transparent images for easy overlaying', action='store_true')
args = parser.parse_args()

if args.model is None:
    for i, avatar in enumerate(models.namelist):
        print(str(i + 1) + ':' + avatar, end=', ')
    num = -1
    while num > len(models.namelist) or num < 1:
        print('\nSet your model number: ', end='')
        try:
            num = int(input())
        except:
            num = -1
    args.model = models.namelist[num - 1]

print('Loading ' + args.model + ' patcher...')
module = importlib.import_module('models.' + args.model)

if args.input is not None:
    patcher = module.patcher(body=args.input)
else:
    patcher = module.patcher()

print('Starting pantie loader...')
pantie_loader = image_loader(fdir='./dream/')

if args.all:
    os.makedirs('./converted/' + args.model, exist_ok=True)
    if args.pantie is not 0:
        pantie_loader.flist = pantie_loader.flist[args.pantie - 1:]
    else:
        if args.force:
            pass
        else:
            pantie_loader.flist = pantie_loader.flist[len(os.listdir('./converted/' + args.model)):]
else:
    pantie_loader.flist = [pantie_loader.flist[args.pantie - 1]]

pantie_loader.start()
for i, fname in enumerate(pantie_loader.flist):
    print('\rProcess: ' + fname + ' [' + str(np.around((i + 1) / len(pantie_loader.flist) * 100, 2)) + '%]', end="")
    patched = patcher.patch(pantie_loader.read(), args.transparent)
    if args.all:
        patcher.save(patched, './converted/' + args.model + '/' + fname)
    else:
        patcher.save(patched, args.output)
