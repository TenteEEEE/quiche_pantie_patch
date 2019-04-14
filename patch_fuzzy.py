from PIL import Image
import os
import sys
import random
import convert_fuzzy as cvt

print("Fuzzy pantie patcher. Options: [-r] Random pantie")
args = sys.argv
panties = os.listdir('./dream/')
add_sign = False
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2fuzzy(fname)
    pantie = Image.open('./fuzzy_pantie.png')
    origin = Image.open('body_fuzzy.png')
    origin.paste(pantie,(845,1595),pantie)
    origin.save('patched_fuzzy.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
