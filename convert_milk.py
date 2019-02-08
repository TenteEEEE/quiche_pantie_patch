import os
import sys
import skimage.io as io
import skimage as ski
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
from myutil import *

def affine_transform(img,mx,my,inv=False):
    [r,c,d] = img.shape
    src_cols = np.linspace(0, c, 10)
    src_rows = np.linspace(0, r, 10)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    shifter_row = np.zeros(src.shape[0])
    shifter_col = np.zeros(src.shape[0])
    if inv:
        line = np.linspace(np.pi, np.pi/2, src.shape[0])
    else:
        line = np.linspace(np.pi/2, np.pi, src.shape[0])
    shifter_row = -(np.sin(line)*mx)
    shifter_col = -(np.sin(line)*my)
    dst_rows = src[:, 1] + shifter_row
    dst_cols = src[:, 0] + shifter_col
    dst = np.vstack([dst_cols, dst_rows]).T
    affin = skt.PiecewiseAffineTransform()
    affin.estimate(src,dst)
    return skt.warp(img, affin)

def convert2milk(fname=None):
    panties = os.listdir('./dream/')
    if fname is None:
        fname =  input("Type pantie name: ./dream/")
    if fname in panties:
        pantie = io.imread('./dream/'+fname)
        mask = io.imread('./mask/mask_milk.png')
        pantie = np.bitwise_and(pantie,mask)
        [r,c,d] = pantie.shape
        front = pantie[:160+30,:200,:]
        back = pantie[:300,200:,]
        patch = pantie[-100:-5,546:,:][::-1,::-1,:]

        # Front and front patch pre-processing
        front = resize(front,(2,2))
        patch = resize(patch,(1.0,1.15))
        [fr,fc,_] = front.shape
        [pr,pf,_] = patch.shape
        patch_pad = np.zeros((fr,fc,d))
        patch_pad[-pr:,:pf,:] = patch
        patch_pad = perspective_transform(patch_pad, np.matrix('1, 0, 0; 0, 1, 0; -0.002,0,1'))
        patch_pad = patch_pad[-pr-40:,:pf-20,:][:,::-1,:]
        [pr,pf,_] = patch_pad.shape

        # Alpha blending and transform between front and front patch
        remain = front[-pr:,:pf,:]*np.float32(skm.dilation(patch_pad[:,:,-1]==0))[:,:,np.newaxis]
        nonzeromask = np.logical_or(skm.dilation(patch_pad[:,:,-1]==1),remain[:,:,-1]==1)
        patch_pad = remain + patch_pad
        normalizer = patch_pad[:,:,-1][:,:,np.newaxis]
        normalizer[normalizer==0] = 1
        patch_pad = patch_pad/normalizer
        patch_pad[:,:,-1] = np.float32(nonzeromask)
        front[-pr:,:pf,:] = patch_pad
        front = perspective_transform(front, np.matrix('1, 0, 0; 0, 1, 0; -0.001,0,1'))
        front = front[:,:-120,:]
        front = affine_transform(front,30,0,inv=True)

        # Back transform
        back = resize(back,(1.3,1.3))[:,::-1,:]
        back = perspective_transform(back, np.matrix('1, 0, 0; 0, 1, 0; 0.0002,0,1'))[:,::-1,:]
        back = affine_transform(back,70,150,inv=False)
        back = back[:,138:,:]

        [fr,fc,_] = front.shape
        [br,bc,_] = back.shape
        pantie = np.zeros((np.max([fr,br]),fc+bc-2,d))
        shiftr = 35
        row_point = np.clip(shiftr+fr,0,np.max([fr,br]))
        pantie[shiftr:row_point,:fc,:] = front[:-(shiftr+fr-row_point),:,:]
        pantie[:bc,fc-1:,:] = back[:,1:,:]
        # io.imshow(pantie)

        # Finalize
        io.imsave('milk_pantie.png',np.uint8(pantie*255))
    else:
        print("Cannot find it")
        
if __name__ == '__main__':
    convert2milk()
