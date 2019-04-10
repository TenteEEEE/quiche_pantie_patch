from PIL import Image
import os
import sys
import random
import convert_ukon as cvt

print("Ukon pantie patcher. Options: [-r] Random pantie")
args = sys.argv
panties = os.listdir('./dream/')
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2ukon(fname)
    pantie = Image.open('./ukon_pantie.png')
    origin = Image.open('body_ukon.png')
    origin.paste(pantie,(616,686),pantie)
    origin.save('patched_ukon.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
