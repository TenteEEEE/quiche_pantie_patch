from PIL import Image
import os
import sys
import random

args = sys.argv
panties = os.listdir('./dream/')
if len(args)>1 and args[1] == '-r':
    num = random.randint(0,len(panties))
    fname = panties[num]
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    pantie = Image.open('./dream/'+fname)
    origin = Image.open('body.png')

    origin.paste(pantie,(1018,828),pantie)
    origin.save('patched.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
