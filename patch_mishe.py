from PIL import Image
import os
import sys
import random
import convert_mishe as cvt

print("Mishe pantie patcher. Options: [-r] Random pantie")
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
    cvt.convert2mishe(fname)
    pantie = Image.open('./mishe_pantie.png')
    origin = Image.open('body_mishe.png')
    if add_sign:
        sign = Image.open('./material/anna_sign.png')
        sign = sign.resize((369,746))
        origin.paste(sign,(933,1482),sign)
    origin.paste(pantie,(910,1929),pantie)
    origin.save('patched_mishe.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
