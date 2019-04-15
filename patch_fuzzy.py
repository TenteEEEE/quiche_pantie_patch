from PIL import Image
import os
import sys
import random
import convert_fuzzy as cvt

print("Fuzzy pantie patcher. Options: [-r] Random pantie, [-f] Enable frill correction")
args = sys.argv
panties = os.listdir('./dream/')
add_sign = False
frill_correction = False
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
    if '-f' in args[1:]:
        frill_correction = True
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2fuzzy(fname, frill_correction)
    pantie = Image.open('./fuzzy_pantie.png')
    origin = Image.open('body_fuzzy.png')
    origin.paste(pantie,(845,1593),pantie)
    origin.save('patched_fuzzy.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
