import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_inabikini.png', **options):
        super().__init__('ビキニ(いな屋さん)', body=body, pantie_position=[-18, 456], **options)
        self.mask = io.imread('./mask/mask_inabikini.png')
        self.bra_mask = io.imread('./mask/mask_inabikini_bra.png')

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_texture(self, image, size):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3]
        front_color = self.pick_color(front)
        front_color = np.append(front_color, 255).astype(np.uint8)
        texture = np.ones((size[0], size[1], 4),  dtype=np.uint8) * front_color
        return Image.fromarray(texture)

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-100:-5, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] + 30, patch.shape[1]), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        front = pantie[:350, :300]
        arrx = (np.linspace(0, 1, 25)**2) * 80
        arrx[4:16] += np.sin(np.linspace(0, np.pi, 12)) * 15
        arrx -= 50
        arry = np.zeros(25)
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(front[:, 7:] * 255)

        back = pantie[:350, 270:-10][::-1, ::-1]
        arrx = (np.linspace(0, 1, 25)**2) * -65
        arrx += 70
        arry = np.zeros(25)
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(back[:-60, 7:] * 255)

        front = np.pad(front, [(0, 0), (0, back.shape[1] - front.shape[1]), (0, 0)], mode='constant')
        pantie = np.concatenate((front[:-68], back), axis=0)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)

    def gen_bra(self, image, fliplr=False):
        pantie = np.array(image)
        bra = pantie[15:170, -200:][::-1, :]
        bra = np.uint8(resize(bra, [1.73, 1.73]) * 255)
        bra = np.bitwise_and(bra, self.bra_mask)
        return Image.fromarray(bra[:, ::-1] if fliplr else bra)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.gen_texture(image, (self.body_size[0], self.body_size[1])), [0, 0])
        patched = self.paste(patched, self.gen_bra(image, fliplr=True), [676, 691])
        patched = self.paste(patched, self.gen_bra(image), [372, 573])
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
