import os
import sys
import random
import argparse
import shutil
import copy
import time
from PIL import Image

parser = argparse.ArgumentParser(description='This script convert all the panties')
parser.add_argument("character", choices=['anna', 'anna_light', 'shaclo', 'milk', 'lua', 'ukon', 'mishe','fuzzy'])
parser.add_argument("--start", type=int, default=1, help='Start num')
parser.add_argument("--pad", action="store_true", help='Padding')
parser.add_argument("--sign", action="store_true", help='Add sign')
parser.add_argument("--frill", action="store_true", help='Enable frill correction for Fuzzy')
args = parser.parse_args()
os.makedirs('converted',exist_ok=True)

if args.character=='fuzzy':
    from convert_fuzzy import *
    converter = convert2fuzzy
    fname = 'fuzzy_pantie.png'
    if args.frill:
        print("Apply frill correction")
    if args.pad:
        pos = (845,1593)
        base = Image.new('RGBA', (4096,4096))
if args.character=='mishe':
    from convert_mishe import *
    converter = convert2mishe
    fname = 'mishe_pantie.png'
    if args.pad:
        pos = (910,1929)
        base = Image.new('RGBA', (4096,4096))
        if args.sign:
            sign = Image.open('./material/anna_sign.png')
            sign = sign.resize((369,746))
            pos_sign = (933,1482)
if args.character=='ukon':
    from convert_ukon import *
    converter = convert2ukon
    fname = 'ukon_pantie.png'
    if args.pad:
        pos = (616,686)
        base = Image.new('RGBA', (1024,1024))
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
if args.character=='anna_light':
    from convert_anna_light import *
    converter = convert2annalight
    fname = 'anna_light_pantie.png'
    if args.pad:
        pos = (0,15)
        base = Image.new('RGBA', (1024,1024))
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
os.makedirs('./converted/'+args.character,exist_ok=True)
for pantie in panties[args.start-1:]:
    print("Process: " + pantie)
    if args.frill:
        converter(pantie, args.frill)
    else:
        converter(pantie)
    if args.pad:
        pantie_img = Image.open(fname)
        base_img = copy.deepcopy(base)
        if args.sign:
            base_img.paste(sign,pos_sign,sign)
        base_img.paste(pantie_img,pos,pantie_img)
        base_img.save(fname)
    time.sleep(0.5)
    os.rename(fname,pantie)
    shutil.move(pantie,'converted/'+args.character+'/'+pantie)
    
    
