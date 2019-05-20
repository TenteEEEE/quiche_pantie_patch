from PIL import Image, ImageOps
import os
import sys
import random
import time
import shutil

args = sys.argv
panties = os.listdir('./dream/')
fname = None
flinz = False
fnbody = False
flight = False
fall = False

if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    if '-l' in args[1:]:
        flinz = True
    if '-n' in args[1:]:
        fnbody = True
    if '-L' in args[1:]:
        flight = True
    if '-a' in args[1:]:
        fall= True
if fname is None and fall is False:
    fname =  input("Type pantie name: ./dream/")
    if fname in panties:
        panties = []
        panties.append(fname)
    else:
        print("Cannot find it")
        exit()
    
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
    
for fname in panties:
    pantie = Image.open('./dream/'+fname)
    if flight:
        origin = Image.open('body_light.png')
    else:
        origin = Image.open('body.png')
    
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
    origin.save('patched.png')
    if fall:
        print('Done ' + fname)
        time.sleep(0.5)
        os.rename('patched_transparent.png', fname)
        shutil.move(fname,fdir+fname)
    else:
        print("Done. Please check patched.png.")
