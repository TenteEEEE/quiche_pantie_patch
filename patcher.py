import os
import sys
import argparse
import importlib
from src.image_loader import *
sys.path.append('./src/')
import avatars

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', help='Choose your model', choices=avatars.namelist)
parser.add_argument('-a', '--all', help='If you set pantie number, it will be start number',  action='store_true')
parser.add_argument('-i', '--input', help='Name of the base texture', type=str)
parser.add_argument('-o', '--output', help='Name of the patched texture', type=str, default='patched.png')
parser.add_argument('-p', '--pantie', help='Choose pantie number', type=int, default=-1)
parser.add_argument('-t', '--transparent', help='Make transparent images for easy overlaying', action='store_true')
args = parser.parse_args()

if args.model is None:
    for i, avatar in enumerate(avatars.namelist):
        print(str(i + 1) + ':' + avatar, end=', ')
    num = -1
    while num > len(avatars.namelist) or num < 1:
        print('\nSet your model number: ', end='')
        try:
            num = int(input())
        except:
            num = -1
    args.model = avatars.namelist[num - 1]

print('Loading ' + args.model + ' patcher...')
module = importlib.import_module('avatars.' + args.model)
patcher = module.patcher()
print('Starting pantie loader...')
pantie_loader = image_loader(fdir='./dream/')

if args.all:
    os.makedirs('./converted/' + args.model, exist_ok=True)
    if args.pantie is not -1:
        pantie_loader.flist = pantie_loader.flist[args.pantie - 1:]
else:
    pantie_loader.flist = [pantie_loader.flist[args.pantie]]

for fname in pantie_loader.flist:
    print('Process: ' + fname)
    patched = patcher.patch(pantie_loader.read(fname), args.transparent)
    if args.all:
        patcher.save(patched, './converted/' + args.model + '/' + fname)
    else:
        patcher.save(patched, args.output)
