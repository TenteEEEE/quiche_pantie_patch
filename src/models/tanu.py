import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_tanu.png'):
        super().__init__('Tanu', body=body, pantie_position=[55, 35])

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-180:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (200, 65), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        # Front affine transform
        front = pantie[:, :300]
        front = np.pad(front, [(100, 00), (100, 100), (0, 0)], mode='constant')
        [r, c, d] = front.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = np.cos(np.linspace(0, 2 * np.pi, src.shape[0]) + np.pi / 8) * 10
        shifter_row[50:] = np.sin(np.linspace(0, 1 * np.pi, 50)) * 20
        shifter_row[70:] += np.sin(np.linspace(0, 1 * np.pi, 30)) * 20
        shifter_col = np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 4) * -50
        shifter_row = np.convolve(shifter_row, np.ones(20) / 20, mode='valid')
        shifter_row = skt.resize(shifter_row, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]
        dst_rows = src[:, 1] + shifter_row
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        front = skt.warp(front, affin)
        front = skt.rotate(front, -15)
        front = front[60:-100, 60:-10, :]
        front = skt.resize(front, (int(front.shape[0] * 1.4), int(front.shape[1] * 1.4)), anti_aliasing=True, mode='reflect')

        # First back affine transform
        back = pantie[:, 300:]
        back = np.pad(back, [(100, 100), (100, 100), (0, 0)], mode='constant')
        [r, c, d] = back.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 2) * 120
        dst_rows = src[:, 1] + shifter_row
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin.estimate(src, dst)
        back = skt.rotate(skt.warp(back, affin), 34, resize=True)

        # Second back affine transform
        [r, c, d] = back.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = np.sin(np.linspace(0, 2 * np.pi, src.shape[0]) + np.pi / 10) * -40
        shifter_row[:25] += np.cos(np.linspace(0, 0.5 * np.pi, 25)) * 88  # left up
        shifter_row[25:45] -= np.sin(np.linspace(0, 1 * np.pi, 20)) * 5  # center up
        shifter_row = np.convolve(shifter_row, np.ones(20) / 20, mode='valid')
        shifter_row = skt.resize(shifter_row, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]
        dst_rows = src[:, 1] + shifter_row
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin.estimate(src, dst)
        back = skt.warp(back, affin)
        back = back[180:-380, 80:-150]
        back = skt.resize(back, (int(back.shape[0] * 1.45), int(back.shape[1] * 1.43)), anti_aliasing=True, mode='reflect')

        front = front[:, :-8]
        back = back[:, 5:]
        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        shiftc = 8
        pantie = np.zeros((np.max([fr, br]), fc + bc - shiftc, d))
        pantie[:br, -bc:] = back
        pantie[:fr, :fc] = front

        # Finalize
        pantie = np.uint8(pantie * 255)
        return Image.fromarray(pantie)
