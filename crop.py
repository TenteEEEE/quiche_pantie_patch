from PIL import Image
import os

fdir = './data/'
mask = Image.open('./mask/mask.png')

panties = os.listdir(fdir)
dreams = os.listdir('./dream/')
start_num = len(dreams)+1
for fname in panties:
    # img = Image.open('./data/Quiche_body.png')
    img = Image.open(fdir+fname)
    zeroimg = Image.new("RGB", img.size, 0)

    masked = Image.composite(img, zeroimg, mask)
    masked.putalpha(mask)
    masked = masked.crop((1018,828,1646,1235))
    masked.save('./dream/%04d.png'%(start_num))
    print('Saved ./dream/%04d.png'%(start_num))
    start_num += 1
