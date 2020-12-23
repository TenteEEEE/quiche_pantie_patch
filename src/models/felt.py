import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_felt.png', **options):
        super().__init__('フェルト', body=body, pantie_position=[11, 633], **options)
        self.mask = io.imread('./mask/mask_felt.png')
        self.bra = io.imread('./mask/bra_felt.png') / 255
        self.bra_shade = io.imread('./material/bra_felt_shade.png') / 255
        self.bra_position = [65, 38]

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[-120:, 546:] = 0
        pantie[125:125 + pr, :pc, :] = patch
        pantie = pantie[:-100]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * -29
        front = pantie[:220, :360]
        front = resize(affine_transform_by_arr(front, arrx, arry), [.75, .75])[:, 5:]
        back = pantie[:, 268:][:, ::-1]
        back = resize(affine_transform_by_arr(back, arrx, arry), [.75, .75])[:, 5:]
        front = np.uint8(front * 255)
        back = np.uint8(back * 255)

        front = np.concatenate([front[:, ::-1], front], axis=1)
        back = np.concatenate([back[:, ::-1], back], axis=1)
        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        dy = 26
        dx = 2
        pantie = np.zeros([fr + br + dy, fc + dx, d], dtype=np.uint8)
        pantie[:fr, dx:dx + fc] = front
        pantie[fr + dy:, :bc] = back
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_bra(self, image):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        front_shade_color = rgb2hsv(front_shade_color[None, None])
        front_shade_color[0, 0, 1] *= front_shade_color[0, 0, 2] / 0.3
        if front_shade_color[0, 0, 1] > 0.7:
            front_shade_color[0, 0, 1] *= 0.7
        front_shade_color[0, 0, 2] *= front_shade_color[0, 0, 2] / 0.4
        front_shade_color = np.clip(hsv2rgb(front_shade_color)[0, 0], 0, 1)

        # painting colors
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color

        # overlaying layers
        bra = alpha_brend(bra_shade, bra, self.bra_shade[:, :, -1])
        bra = np.dstack((bra, self.bra[:, :, -1]))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        return patched
