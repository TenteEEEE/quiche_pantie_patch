from PIL import Image
import os
import sys
import random

args = sys.argv
panties = os.listdir('./dream/')
fname = None
flinz = False
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    if '-l' in args[1:]:
        flinz = True
if fname is None:
    fname =  input("Type pantie name: ./dream/")
    
if fname in panties:
    pantie = Image.open('./dream/'+fname)
    origin = Image.open('body.png')

    if flinz:
        print("Apply LINZ Correction")
        pantie = pantie.resize((629,407))
        origin.paste(pantie,(1017,828),pantie)
    else:
        origin.paste(pantie,(1018,828),pantie)
    origin.save('patched.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
