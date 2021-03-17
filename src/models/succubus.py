from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_koyuki.png', **options):
        super().__init__('サキュバス', body=body, pantie_position=[1994, 193], **options)
        self.back_position = [2650, 21]
        self.right_position = [68, 103]
        self.mask_front = io.imread('./mask/mask_succubus_front.png')
        self.mask_back = io.imread('./mask/mask_succubus_back.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-150:-5, 546:, :])
        patch = np.uint8(resize(patch, [1.2, 1.]) * 255)
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch[::-1, ::-1]
        pantie[-150:, 546:, :] = 0
        pantie = pantie[:300]
        pantie = resize(pantie, [2.35, 2.35])
        pantie = np.uint8(pantie * 255)
        front = pantie[:, :765]
        front = np.uint8(resize(front, [0.77, 1]) * 255)
        front = np.bitwise_and(front, self.mask_front)
        back = pantie[:, 752:-18]
        back = np.bitwise_and(back, self.mask_back)
        back = np.concatenate([back, back[:, ::-1]], axis=1)
        return Image.fromarray(front), Image.fromarray(back)

    def patch(self, image, transparent=False):
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        front, back = self.convert(image)
        patched = self.paste(patched, back, self.back_position)
        patched = self.paste(patched, front, self.pantie_position)
        patched = self.paste(patched, ImageOps.mirror(front), self.right_position)
        return patched
