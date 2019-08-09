import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *

class patcher(patcher):
    def __init__(self, body='./body/body_yuko.png', **options):
        super().__init__('Yuko', body=body, pantie_position=[910, 1929], **options)

    def convert(self, image):
        image = Image.open('./dream/0200.png')
        pantie = np.array(image)

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (230, 65), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        front = pantie[:350, :250, :]
        back = pantie[:350, 250:, :]
        # front = np.pad(front, [(0, 0), (100, 130), (0, 0)], mode='constant')

        # Affine transform matrix
        [r, c, d] = pantie.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        # shifter_row[30:-30] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 32) * 100)[30:-30]
        # shifter_row[:30] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 2) * 60)[:30]
        # shifter_row[-30:] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 2) * 80)[-30:]
        # shifter_col[13:-30] = -(np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 8) * 22)[13:-30]

        # shifter_row = np.convolve(shifter_row, np.ones(20) / 20, mode='valid')
        # shifter_col = np.convolve(shifter_col, np.ones(10) / 10, mode='valid')
        # shifter_row = skt.resize(shifter_row, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]
        # shifter_col = skt.resize(shifter_col, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]

        dst_rows = src[:, 1] + shifter_row
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        # pantie = np.uint8(skt.warp(pantie, affin) * 255)[:310, :, :]
        pantie_ = np.uint8(skt.warp(pantie, affin) * 255)
        io.imshow(pantie_)

        # Finalize
        pantie_ = skt.resize(pantie, (np.int(pantie.shape[0] * 2.05), np.int(pantie.shape[1] * 2.05)), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie_ * 255)
        return Image.fromarray(pantie)
