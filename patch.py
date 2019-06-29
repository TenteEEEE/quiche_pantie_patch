from PIL import Image, ImageOps
import os
import sys
import random
import time
import shutil
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('-r', '--random', help='ランダムでパンツが選ばれます', action='store_true')
argparser.add_argument('-l', '--linz', help='リンツちゃん向けの微補正を加えます', action='store_true')
argparser.add_argument('-n', '--nude', help='キッシュ/リンツちゃん素体用のオプションです', action='store_true')
argparser.add_argument('-L', '--light', help='キッシュちゃんライト用のオプションです', action='store_true')
argparser.add_argument('-a', '--all', help='全てのパンツを変換します', action='store_true')
argparser.add_argument('-i', '--input', help='ベースとなるテクスチャを指定できます', type=str)
argparser.add_argument('-o', '--output', help='変換後の名前を指定できます', type=str, default='patched.png')
argparser.add_argument('-p', '--pantie', help='変換するパンツの番号を数値で指定できます', type=int)
args = argparser.parse_args()

panties = os.listdir('./dream/')

if args.random:
    num = random.randint(0,len(panties))
    fname = panties[num]
flinz = args.linz
fnbody = args.nude
flight = args.light
fall= args.all
fname = args.pantie
fin = args.input
fout = args.output

if fall:
    if flinz:
        fdir = 'converted/linz/'
    elif fnbody:
        fdir = 'converted/quiche_n/'
    elif flight:
        fdir = 'converted/quiche_light/'
    else:
        fdir = 'converted/quiche/'
    os.makedirs(fdir,exist_ok=True)
    exists = len(os.listdir(fdir))
    panties = panties[exists:]
else:
    if fname is not None:
        fname = "{:04}.png".format(fname)        
    else:
        fname =  input("Type pantie name: ./dream/")
    
    if fname in panties:
        panties = []
        panties.append(fname)
    else:
        print("Cannot find it")
        exit()

if fin is not None and os.path.exists(fin):    
    origin_fname = fin
elif flight:
    origin_fname = 'body_light.png'
else:
    origin_fname = 'body.png'
    
for fname in panties:    
    pantie = Image.open('./dream/'+fname)
    origin = Image.open(origin_fname)

    if flinz:
        print("Apply LINZ Correction")
        pantie = pantie.resize((629,407))
        origin.paste(pantie,(1017,828),pantie)
        origin_transparent = Image.new("RGBA", (origin.size))
        origin_transparent.paste(pantie,(1017,828),pantie)
        origin_transparent.save('patched_transparent.png')
    elif fnbody:        
        print("!nbody_mode!")
        cut = 7
        right_pantie = pantie.crop((cut,0,pantie.size[0],pantie.size[1]))
        left_pantie = ImageOps.mirror(right_pantie)
        npantie = Image.new("RGBA", (right_pantie.size[0]*2, right_pantie.size[1]))
        npantie.paste(right_pantie,(right_pantie.size[0],0))
        npantie.paste(left_pantie,(0,0))
        origin.paste(npantie,(403,836),npantie)
        
        origin_transparent = Image.new("RGBA", (origin.size))
        origin_transparent.paste(npantie,(403,836),npantie)
        origin_transparent.save('patched_transparent.png')
    elif flight:
        print("Apply Quiche_Light Conversion")
        pantie = pantie.resize((236,157))
        origin.paste(pantie,(532,385),pantie)
        origin_transparent = Image.new("RGBA", (origin.size))
        origin_transparent.paste(pantie,(532,385),pantie)
        origin_transparent.save('patched_transparent.png')
    else:
        origin.paste(pantie,(1018,828),pantie)
        origin_transparent = Image.new("RGBA", (origin.size))
        origin_transparent.paste(pantie,(1018,828),pantie)
        origin_transparent.save('patched_transparent.png')

    origin.save(fout)

    if fall:
        print('Done ' + fname)
        time.sleep(0.5)
        os.rename('patched_transparent.png', fname)
        shutil.move(fname,fdir+fname)
    else:
        print("Done. Please check {}.".format(fout))
