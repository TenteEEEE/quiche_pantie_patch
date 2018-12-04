from PIL import Image
import os

panties = os.listdir('./dream/')
fname =  input("Type pantie name: ./dream/")

if fname in panties:
    pantie = Image.open('./dream/'+fname)
    origin = Image.open('body.png')

    origin.paste(pantie,(1018,828),pantie)
    origin.save('test.png')
