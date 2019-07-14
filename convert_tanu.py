import os
import sys
import skimage.io as io
import skimage as ski
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
from myutil import *
import matplotlib.pyplot as plt

def convert2tanu(fname=None):
panties = os.listdir('./dream/')
fname = panties[101]
if fname is None:
    fname =  input("Type pantie name: ./dream/")
if fname in panties:
    pantie = io.imread('./dream/'+fname)
    
    patch = np.copy(pantie[-180:-5,546:,:])
    patch = skt.resize(patch[::-1,::-1,:],(200,65),anti_aliasing=True,mode='reflect')
    [pr,pc,d] = patch.shape
    pantie[127-5:127-5+pr,:pc,:] = np.uint8(patch*255)
    
    # Front affine transform
    front = pantie[:,:300]
    front = np.pad(front,[(100,00),(100,100),(0,0)],mode='constant')
    [r,c,d] = front.shape
    src_cols = np.linspace(0, c, 10)
    src_rows = np.linspace(0, r, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    shifter_row = np.zeros(src.shape[0])
    shifter_col = np.zeros(src.shape[0])
    shifter_row = np.sin(np.linspace(0, 2 * np.pi, src.shape[0])-np.pi/8)*-20
    shifter_col = np.sin(np.linspace(0, 1 * np.pi, src.shape[0])-np.pi/8)*-50
    dst_rows = src[:, 1] + shifter_row
    dst_cols = src[:, 0] + shifter_col
    dst = np.vstack([dst_cols, dst_rows]).T
    affin = skt.PiecewiseAffineTransform()
    affin.estimate(src,dst)
    front = skt.warp(front, affin)
    front = skt.rotate(front,-15)
    io.imsave('a1.png',front)
    io.imshow(front)
    # front = front[70:-90,60:-20,:]
    # front = skt.resize(front,(front.shape[0]*1.42,front.shape[1]*1.47),anti_aliasing=True,mode='reflect')
    
    # First back affine transform
    back = pantie[:,300:]
    back = np.pad(back,[(100,100),(100,100),(0,0)],mode='constant')    
    [r,c,d] = back.shape
    src_cols = np.linspace(0, c, 10)
    src_rows = np.linspace(0, r, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    shifter_row = np.zeros(src.shape[0])
    shifter_col = np.zeros(src.shape[0])
    shifter_row = np.sin(np.linspace(0, 1 * np.pi, src.shape[0])+np.pi/2)*120
    dst_rows = src[:, 1] + shifter_row
    dst_cols = src[:, 0] + shifter_col
    dst = np.vstack([dst_cols, dst_rows]).T
    affin.estimate(src,dst)
    back = skt.rotate(skt.warp(back, affin),34,resize=True)
    
    # Second back affine transform
    [r,c,d] = back.shape
    io.imshow(back)
    src_cols = np.linspace(0, c, 10)
    src_rows = np.linspace(0, r, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    shifter_row = np.zeros(src.shape[0])
    shifter_col = np.zeros(src.shape[0])
    shifter_row = np.sin(np.linspace(0, 2 * np.pi, src.shape[0])+np.pi/10)*-20
    shifter_row[25:45] += np.sin(np.linspace(0, 1 * np.pi, 20))*-45
    shifter_row = np.convolve(shifter_row,np.ones(20)/20,mode='valid')
    shifter_row = skt.resize(shifter_row,(100,1),anti_aliasing=True,mode='reflect')[:,0];
    
    plt.plot(shifter_row)
    dst_rows = src[:, 1] + shifter_row
    dst_cols = src[:, 0] + shifter_col
    dst = np.vstack([dst_cols, dst_rows]).T
    affin.estimate(src,dst)
    back = skt.warp(back,affin)
    
    skt.resize(pantie,(np.int(pantie.shape[0]*2.05),np.int(pantie.shape[1]*2.05)),anti_aliasing=True,mode='reflect')

    # Finalize
    io.imsave('milk_pantie.png',np.uint8(pantie*255))
else:
    print("Cannot find it")
        
if __name__ == '__main__':
    convert2tanu()
