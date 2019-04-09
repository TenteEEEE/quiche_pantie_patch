import os
import sys
import skimage.io as io
import skimage as ski
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
from myutil import *

def convert2ukon(fname=None):
    panties = os.listdir('./dream/')
    if fname is None:
        fname =  input("Type pantie name: ./dream/")
    if fname in panties:
        pantie = io.imread('./dream/'+fname)
        mask = io.imread('./mask/mask_ukon.png')
        pantie = np.bitwise_and(pantie,mask)


        front = pantie[:153,:178,:]
        front = resize(front,[0.84,0.835])[:,:,:]

        back = pantie[:284,355:627,:]
        back = skt.rotate(back, 180)
        back = resize(back,[0.52,0.55])

        [fr,fc,_] = front.shape
        [br,bc,_] = back.shape
        pantie = np.zeros((fr+br,np.max([fc,bc]),4))
        pantie[:fr,:fc,:] = front
        pantie[fr:,:bc,:] = back

        # Finalize
        io.imsave('ukon_pantie.png',pantie)

    else:
        print("Cannot find it")
        
if __name__ == '__main__':
    convert2ukon()
