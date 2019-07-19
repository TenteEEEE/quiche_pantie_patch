import os
import sys
import numpy as np
import argparse
import importlib
import random
import json
from src.image_loader import image_loader
sys.path.append('./src/')
import models

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', help='Choose your model', choices=models.models_namelist)
parser.add_argument('-a', '--all', help='If you set pantie number, it will be start number and works with force overwriting',  action='store_true')
parser.add_argument('-f', '--force', help='Overwrite the patched textures even if it exists',  action='store_true')
parser.add_argument('-i', '--input', help='Name of the base texture', type=str)
parser.add_argument('-o', '--output', help='Name of the patched texture', type=str, default='patched.png')
parser.add_argument('-p', '--pantie', help='Choose pantie number [default: latest]', type=int, default=0)
parser.add_argument('-d', '--directory', help='Output directory name when you set all flag', type=str, default='default')
parser.add_argument('-t', '--transparent', help='Make transparent images for easy overlaying', action='store_true')
parser.add_argument('-r', '--random', help='It chooses a pantie randomly', action='store_true')
parser.add_argument('-j', '--json', help='Load favorite.json When you set it, all arguments are ignored', action='store_true')
args = parser.parse_args()

if args.json:
    print('Loading your favorite.json...')
    f = open('./favorite.json',mode='r')
    options = json.load(f)
    args.model = options['model']
    args.all = options['all']
    args.force = options['force']
    args.input = options['input']
    args.output = options['output']
    args.pantie = options['pantie']
    args.transparent = options['transparent']
    args.random = options['random']
    args.directory = options['directory']

if args.model is None:
    for i, avatar in enumerate(models.models_namelist):
        print(str(i + 1) + ':' + avatar, end=', ')
    num = -1
    while num > len(models.models_namelist) or num < 1:
        print('\nSet your model number: ', end='')
        try:
            num = int(input())
        except:
            num = -1
    args.model = models.models_namelist[num - 1]

print('Loading ' + args.model + ' patcher...')
module = importlib.import_module('models.' + args.model)

if args.input is not None:
    if args.json:
        patcher = module.patcher(body=args.input,options=options)
    else:
        patcher = module.patcher(body=args.input)    
else:
    if args.json:
        patcher = module.patcher(options=options)
    else:
        patcher = module.patcher()

print('Starting pantie loader...')
pantie_loader = image_loader(fdir='./dream/')

if args.all:
    if args.directory == 'default':
        outdir = './converted/' + args.model
    else:
        outdir = './converted/' + args.directory
    os.makedirs(outdir, exist_ok=True)

    if args.pantie is not 0:
        pantie_loader.flist = pantie_loader.flist[args.pantie - 1:]
    else:
        if args.force:
            pass
        else:
            pantie_loader.flist = pantie_loader.flist[len(os.listdir(outdir)):]
else:
    if args.random:
        pantie_loader.flist = [pantie_loader.flist[random.randint(0,len(pantie_loader.flist))]]
    else:
        pantie_loader.flist = [pantie_loader.flist[args.pantie - 1]]

pantie_loader.start()
for i, fname in enumerate(pantie_loader.flist):
    print('\rProcess: ' + fname + ' [' + str(np.around((i + 1) / len(pantie_loader.flist) * 100, 2)) + '%]', end="")
    patched = patcher.patch(pantie_loader.read(), args.transparent)
    if args.all:
        patcher.save(patched, outdir + '/' + fname)
    else:
        patcher.save(patched, args.output)
