import os
import sys
import skimage.io as io
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
from myutil import *

def convert2annalight(fname=None):
    panties = os.listdir('./dream/')
    if fname is None:
        fname =  input("Type pantie name: ./dream/")
    if fname in panties:
        pantie = io.imread('./dream/'+fname)
        [r,c,d] = pantie.shape
        
        # move from hip to front
        patch = np.copy(pantie[-170:,546:,:])
        pantie[-100:,546:,:] = 0
        patch = skt.resize(patch[::-1,::-1,:],(patch.shape[0],50),anti_aliasing=True,mode='reflect')
        [pr,pc,d] = patch.shape
        pantie[137:137+pr,:pc,:] = np.uint8(patch*255)
        pantie = pantie[:-165,:,:]

        # Finalize
        pantie = skt.resize(pantie,(np.int(pantie.shape[0]*0.405),np.int(pantie.shape[1]*0.405)),anti_aliasing=True,mode='reflect')
        io.imsave('anna_light_pantie.png',np.uint8(pantie*255)[:,2:,:])
    else:
        print("Cannot find it")
        
if __name__ == '__main__':
    convert2annalight()
