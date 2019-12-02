import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_phyri.png', **options):
        super().__init__('フィリ', body=body, pantie_position=[2437, 353], **options)
        self.mask = io.imread('./mask/mask_phyri.png')

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:145, :380]
        front = (resize(front, [0.85, 0.85]) * 255).astype(np.uint8)

        back = pantie[:-7, 340:]
        back = np.rot90(back, 1)
        back = np.pad(back, [(0, 0), (0, 200), (0, 0)], mode='constant')
        arrx = np.zeros(100)
        arry = np.linspace(0, 1, 100)**3 * -155
        back = affine_transform_by_arr(back, arrx, arry)[:, :-140]
        back = (resize(back, [0.71, 0.71]) * 255).astype(np.uint8)
        back = np.rot90(back, 1)

        def alpha_brend(img1, img2, mask):
            return img1 * mask[:, :, None] + img2 * (1 - mask)[:, :, None]
        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shift_y = 9
        pantie = np.zeros((fr + br - shift_y, np.max((fc, bc)), d), dtype=np.uint8)
        pantie[:fr, :fc] = front
        pantie[fr - shift_y:fr + br - shift_y, :bc] = alpha_brend(back, pantie[fr - shift_y:fr + br - shift_y, :bc], back[:, :, -1] > 250)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, image, self.pantie_position)
        patched = self.paste(patched, ImageOps.mirror(image), (self.body_size[0] - self.pantie_position[0] - image.size[0], self.pantie_position[1]))
        return patched
