import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_mishe.png', add_sign=None, fsign='./material/anna_sign.png'):
        super().__init__('Mishe', body=body, pantie_position=[910, 1929])
        self.mask = io.imread('./mask/mask_mishe.png')
        self.sign_position = [933, 1482]
        if add_sign is None:
            self.add_sign = self.ask(question='Add immoral sign?', default=False)
        else:
            self.add_sign = add_sign
        if self.add_sign:
            self.sign = Image.open(fsign)
            self.sign = self.sign.resize((369,746))

    def convert(self, image):
        pantie = np.array(image)
        pantie = np.bitwise_and(pantie, self.mask)
        [r, c, d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        pantie[-115:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 63), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        # Affine transform matrix
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row[30:-30] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 32) * 100)[30:-30]
        shifter_row[:30] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 2) * 60)[:30]
        shifter_row[-30:] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 2) * 80)[-30:]
        shifter_col[13:-30] = -(np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 8) * 22)[13:-30]

        shifter_row = np.convolve(shifter_row, np.ones(20) / 20, mode='valid')
        shifter_col = np.convolve(shifter_col, np.ones(10) / 10, mode='valid')
        shifter_row = skt.resize(shifter_row, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]
        shifter_col = skt.resize(shifter_col, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]

        dst_rows = src[:, 1] + shifter_row - 110
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = np.uint8(skt.warp(pantie, affin) * 255)[:310, :, :]

        # Finalize
        pantie_ = skt.resize(pantie, (np.int(pantie.shape[0] * 2.05), np.int(pantie.shape[1] * 2.05)), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie_ * 255)
        return Image.fromarray(pantie)
    
    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        
        if self.add_sign:
            self.paste(patched, self.sign, self.sign_position)
        patched = self.paste(patched, image, self.pantie_position)
        return patched
