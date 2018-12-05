from PIL import Image
import os

fdir = './data/'
mask = Image.open('./mask.png')

panties = os.listdir(fdir)
for fname in panties:
    # img = Image.open('./data/Quiche_body.png')
    img = Image.open(fdir+fname)
    zeroimg = Image.new("RGB", img.size, 0)

    masked = Image.composite(img, zeroimg, mask)
    masked.putalpha(mask)
    masked = masked.crop((1018,828,1646,1235))
    masked.save('./'+fname)
