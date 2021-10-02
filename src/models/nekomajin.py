from numpy.matrixlib.defmatrix import matrix
import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_nekomajin.png', **options):
        super().__init__(name='ねこまじん', body=body, pantie_position=[-20,0], **options)
        self.mask = io.imread('./mask/mask_nekomajin.png')

    def convert(self, image):
        pantie = np.array(image)
        [r, c, d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-200:, 546:, :])
        pantie[-200:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (247, 40), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[160:160 + pr, :pc, :] = np.uint8(patch * 255)
        
        # Affine transform matrix
        matrixCount = 15
        shifter_row = np.sin(np.linspace(0, np.pi * 2, matrixCount) + np.pi / 4) * 35 - 15 #サイン波1周期分をバイアス込で描いて
        shifter_row[(matrixCount//5)*4:] = np.sin(np.linspace(0, np.pi, matrixCount - (matrixCount//5)*4)) * 20 + shifter_row[8]  #お尻の部分をサイン波半周期で上げて
        shifter_row[-(matrixCount//10):] = shifter_row[-(matrixCount//10)-1]  # 最後だけ手入力
        #shifter_row = [5,15,20,10,10,-10,-30,-40,-50,-40,-35,-30,-30,-10,-10]
        src_cols = np.linspace(0, c, matrixCount)
        src_rows = np.linspace(0, r, matrixCount)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        dst_rows = src[:, 1]
        dst_cols = src[:, 0]
        dst = np.vstack([dst_cols, dst_rows]).T
        row = int((dst[1,1]-dst[0,1]) * 0.95) #1マスの最大幅
        for i in range(matrixCount):
            if shifter_row[i] > 0 :
                dst[i*matrixCount+2: (i+1)*matrixCount,1] -= shifter_row[i]
            for j in range(matrixCount - 2):
                if shifter_row[i] < 0 :
                    k = j + 2
                    v = min(-shifter_row[i],row)
                    dst[i*matrixCount+k: (i+1)*matrixCount,1] += v
                    shifter_row[i] += v
        # transform front uv
        dst[2*matrixCount-matrixCount//5:2*matrixCount,0] -= np.linspace(0, 15, matrixCount//5)

        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = np.uint8(skt.warp(pantie, affin) * 255)

        # Finalize
        pantie = skt.resize(pantie, (866,1813), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
