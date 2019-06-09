import os
import sys
import skimage.io as io
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
import matplotlib.pyplot as plt

panties = os.listdir('./dream/')
bra_mask = io.imread('./mask/bra.png')[:430,1024:1024+620,:]
bra_center = io.imread('./mask/bra_center.png')[:430,1024:1024+620,:]
bra_shade = io.imread('./material/bra_shade.png')[:430,1024:1024+620,:]
# plt.imshow(bra_shade)

# fname = panties[59]
fname = panties[100]
pantie = io.imread('./dream/'+fname)
hip = pantie[20:180,-130:]
hip = skt.resize(hip,(np.int(hip.shape[0]*1.6),np.int(hip.shape[1]*1.6)),anti_aliasing=True,mode='reflect')

[r,c,d] = bra_mask.shape
[hr,hc,hd] = hip.shape
posx = 20
posy = 170
padx = c-hc-posx
pady = r-hr-posy
hip = (np.pad(hip,[(posy,pady),(posx,padx),(0,0)],mode='constant')*255).astype(np.uint8)
hip[:,:,3] = bra_center[:,:,0]
plt.imshow(hip)
