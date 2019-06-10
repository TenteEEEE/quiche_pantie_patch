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
[r,c,d] = bra_mask.shape

# fname = panties[59]
fname = panties[100]
pantie = io.imread('./dream/'+fname)

# center painting
center_texture = pantie[20:180,-130:]
center_texture = skt.resize(center_texture,(np.int(center_texture.shape[0]*1.6),np.int(center_texture.shape[1]*1.6)),anti_aliasing=True,mode='reflect')
[hr,hc,hd] = center_texture.shape
posx = 20
posy = 170
padx = c-hc-posx
pady = r-hr-posy
center_texture = (np.pad(center_texture,[(posy,pady),(posx,padx),(0,0)],mode='constant'))
center_texture[:,:,3] = bra_center[:,:,0]

# base color painting
front = pantie[20:100,30:80,:]
# base = np.mean(np.mean(front,axis=0),axis=0)
base = np.median(np.median(front,axis=0),axis=0)/255.0
base_texture = np.copy(bra_mask).astype(np.float32)/255.0
base_texture = (base_texture*base)

# convined them and shading
center_mask = (bra_center[:,:,0][:,:,None]/255.0).astype(np.float32)
convined_texture = base_texture*(1-center_mask) + center_texture*center_mask
convined_texture[:,:,:3] *= bra_shade[:,:,:3].astype(np.float32)/255.0
convined_texture[:,:,3] = (bra_mask[:,:,0]/255.0).astype(np.float32)

# finalize
convined_texture = (convined_texture*255.0).astype(np.uint8)
