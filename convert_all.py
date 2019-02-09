import os
import sys
import random
import argparse
import shutil
import copy
from PIL import Image

parser = argparse.ArgumentParser(description='This script convert all the panties')
parser.add_argument("character", choices=['anna', 'shaclo', 'milk'])
parser.add_argument("--pad", action="store_true", help='Padding')
args = parser.parse_args()
os.makedirs('converted',exist_ok=True)

if args.character=='anna':
    from convert_anna import *
    converter = convert2anna
    fname = 'anna_pantie.png'
    if args.pad:
        pos = (31,1115)
        base = Image.new('RGBA', (2048,2048))
if args.character=='milk':
    from convert_milk import *
    converter = convert2milk
    fname = 'milk_pantie.png'
    if args.pad:
        pos = (741,224)
        base = Image.new('RGBA', (2048,2048))
if args.character=='shaclo':
    from convert_shaclo import *
    converter = convert2shaclo
    fname = 'shaclo_pantie.png'
    if args.pad:
        pos = (62,16)
        base = Image.new('RGBA', (2229,727))

panties = os.listdir('./dream/')
for pantie in panties:
    print("Process: " + pantie)
    converter(pantie)
    if args.pad:
        pantie_img = Image.open(fname)
        base_img = copy.deepcopy(base)
        base_img.paste(pantie_img,pos,pantie_img)
        base_img.save(fname)
    os.rename(fname,pantie)
    shutil.move(pantie,'converted/'+pantie)
    
    
