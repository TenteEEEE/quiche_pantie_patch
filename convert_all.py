import os
import sys
import random
import argparse
import shutil
import copy
from PIL import Image

parser = argparse.ArgumentParser(description='This script convert all the panties')
parser.add_argument("character", choices=['anna', 'shaclo', 'milk', 'lua'])
parser.add_argument("--pad", action="store_true", help='Padding')
parser.add_argument("--sign", action="store_true", help='Add sign')
args = parser.parse_args()
os.makedirs('converted',exist_ok=True)

if args.character=='lua':
    from convert_lua import *
    converter = convert2lua
    fname = 'lua_pantie.png'
    if args.pad:
        pos = (0,1749)
        base = Image.new('RGBA', (4096,4096))
if args.character=='anna':
    from convert_anna import *
    converter = convert2anna
    fname = 'anna_pantie.png'
    if args.pad:
        pos = (31,1115)
        base = Image.new('RGBA', (2048,2048))
        if args.sign:
            sign = Image.open('./material/anna_sign.png')
            pos_sign = (37,861)
if args.character=='milk':
    from convert_milk import *
    converter = convert2milk
    fname = 'milk_pantie.png'
    if args.pad:
        pos = (741,224)
        base = Image.new('RGBA', (2048,2048))
        if args.sign:
            sign = Image.open('./material/anna_sign.png')
            sign = sign.resize((int(sign.width * 0.6), int(sign.height * 0.6)))
            pos_sign = (754,113)
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
        if args.sign:
            base_img.paste(sign,pos_sign,sign)
        base_img.paste(pantie_img,pos,pantie_img)
        base_img.save(fname)
    os.rename(fname,pantie)
    shutil.move(pantie,'converted/'+pantie)
    
    
