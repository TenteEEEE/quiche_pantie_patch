from PIL import Image, ImageOps
import os
import sys
import random

args = sys.argv
panties = os.listdir('./dream/')
fname = None
flinz = False
fnbody = False
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    if '-l' in args[1:]:
        flinz = True
    if '-n' in args[1:]:
        fnbody = True
if fname is None:
    fname =  input("Type pantie name: ./dream/")
    
if fname in panties:
    pantie = Image.open('./dream/'+fname)
    origin = Image.open('body.png')
    
    if flinz:
        print("Apply LINZ Correction")
        pantie = pantie.resize((629,407))
        origin.paste(pantie,(1017,828),pantie)
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
    else:
        origin.paste(pantie,(1018,828),pantie)
    origin.save('patched.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
