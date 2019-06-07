from PIL import Image
import os
import sys
import random
import convert_anna_light as cvt

args = sys.argv
panties = os.listdir('./dream/')
print("Annna light pantie patcher. Options: [-r] Random pantie")
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2annalight(fname)
    pantie = Image.open('./anna_light_pantie.png')
    origin = Image.open('body_anna_light.png')
    origin.paste(pantie,(0,15),pantie)
    origin.save('patched_anna_light.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
