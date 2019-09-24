import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_ramne.png', **options):
        super().__init__(name='ラムネ', body=body, pantie_position=[412, 835], **options)
        self.mask = io.imread('./mask/mask_ramne.png')
        self.sign_position = [844, 666]
        try:
            self.add_sign = self.options['add_sign']
        except:
            self.add_sign = self.ask(question='Add immoral sign?', default=False)
        if self.add_sign:
            try:
                sign = Image.open(self.options['fsign'])
            except:
                sign = Image.open('./material/anna_sign.png')
            left = ImageOps.mirror(sign)
            margin = 25
            self.sign = Image.new("RGBA", (sign.size[0] * 2 + margin, sign.size[1]))
            self.sign.paste(sign, (sign.size[0] + int(margin/2), 0))
            self.sign.paste(left, (0, 0))

    def convert(self, image):
        pantie = np.array(image)
        
        # Rear to front
        patch = np.copy(pantie[-110:-5, 548:, :])[::-1, ::-1, :]
        [pr, pc, d] = patch.shape
        pantie[105:105 + pr, :pc, :] = patch
        pantie = pantie[:-100, :, :]
        pantie = np.pad(pantie, [(100, 0), (0, 0), (0, 0)], mode='constant')
        pantie = perspective_transform(pantie, np.matrix('1, 0.01, 0; 0, 1, 0; -0.0008,0,1'))
        
        # Affine transform
        [r, c, d] = pantie.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 4) * 40)
        shifter_col = -np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 8) * 20
        shifter_row[shifter_row < 0] = 0
        shifter_row = np.convolve(shifter_row, np.ones(10) / 10, mode='valid')
        shifter_row = skt.resize(shifter_row, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]
        shifter_col = np.convolve(shifter_col, np.ones(10) / 10, mode='valid')
        shifter_col = skt.resize(shifter_col, (100, 1), anti_aliasing=True, mode='reflect')[:, 0]
        dst_rows = src[:, 1] + shifter_row
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = skt.warp(pantie, affin)

        # Mirroring
        pantie = pantie[25:290, 19:430, :]
        pantie = skt.resize(pantie, (np.int(pantie.shape[0] * 1.47), np.int(pantie.shape[1] * 1.49)), anti_aliasing=True, mode='reflect')
        pantie = np.bitwise_and(np.uint8(pantie[7:, :, :] * 255), self.mask)
        [r, c, d] = pantie.shape
        npantie = np.zeros((r, c * 2, d), dtype=np.uint8)
        npantie[:, c:, :] = pantie
        npantie[:, :c, :] = pantie[:, ::-1, :]

        return Image.fromarray(npantie)
        
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
