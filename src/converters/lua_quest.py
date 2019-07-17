import os
import sys
import skimage.io as io
import skimage as ski
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
from myutil import *

def convert2luaquest(fname=None):
    panties = os.listdir('./dream/')
    if fname is None:
        fname =  input("Type pantie name: ./dream/")
    if fname in panties:
        pantie = io.imread('./dream/'+fname)
        
        patch = np.copy(pantie[-140:-5,546:,:])
        patch = skt.resize(patch[::-1,::-1,:],(230,65),anti_aliasing=True,mode='reflect')
        [pr,pc,d] = patch.shape
        pantie[127-5:127-5+pr,:pc,:] = np.uint8(patch*255)
        
        front = pantie[:350,:300,:]
        front = np.pad(front,[(0,0),(100,130),(0,0)],mode='constant')    
        front = perspective_transform(front,np.matrix('1, 0.05, 0; 0, 1, 0; 0.0005,0,1'))
        front = perspective_transform(front,np.matrix('1, 0.0, 0; 0, 1, 0; -0.0009,0,1'))
        front = front[:-45,70:335]
        front = resize(front,[1.7,1.7])
        
        back = pantie[:380,300:,:]
        back = np.pad(back,[(15,0),(0,200),(0,0)],mode='constant')
        back =  perspective_transform(back,np.matrix('1, -0.1, 0; 0.01, 1, 0; -0.0006,0,1'))
        back = back[:-70,10:290,:]
        back = resize(back,[1.36,1.36])

        [fr,fc,_] = front.shape
        [br,bc,_] = back.shape
        shift_y = 20
        pantie = np.zeros((np.max([fr,br])+shift_y,fc+bc,d))
        pantie[shift_y:shift_y+fr,:fc,:] = front
        pantie[:br,fc:,:] = back
        pantie = pantie[12:,16:,:]
        mask = io.imread('./mask/mask_lua_quest.png')
        pantie = np.bitwise_and(np.uint8(pantie*255),mask)

        # Finalize
        io.imsave('lua_quest_pantie.png',pantie)
    else:
        print("Cannot find it")
    
if __name__ == '__main__':
    convert2luaquest()
