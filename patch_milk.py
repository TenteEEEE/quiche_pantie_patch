from PIL import Image
import os
import sys
import random
import convert_milk as cvt

print("Milk pantie patcher. Options: [-r] Random pantie, [-s] Add sign")
args = sys.argv
panties = os.listdir('./dream/')
add_sign = False
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
    cvt.convert2milk(fname)
    pantie = Image.open('./milk_pantie.png')
    origin = Image.open('body_milk.png')
    if add_sign:
        sign = Image.open('./material/anna_sign.png')
        sign = sign.resize((int(sign.width * 0.6), int(sign.height * 0.6)))
        origin.paste(sign,(754,113),sign)
    origin.paste(pantie,(741,224),pantie)
    origin.save('patched_milk.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
