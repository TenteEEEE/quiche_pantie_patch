from PIL import Image
import os
import sys
import random
import convert_anna as cvt

args = sys.argv
panties = os.listdir('./dream/')
add_sign = False
print("Annna pantie patcher. Options: [-r] Random pantie, [-s] Add sign")
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
    if '-s' in args[1:]:
        add_sign = True
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2anna(fname)
    pantie = Image.open('./anna_pantie.png')
    origin = Image.open('body_anna.png')
    if add_sign:
        sign = Image.open('./material/anna_sign.png')
        origin.paste(sign,(37,861),sign)
    origin.paste(pantie,(31,1115),pantie)
    origin.save('patched_anna.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
