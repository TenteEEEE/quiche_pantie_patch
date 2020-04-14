import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_k2under1.png', **options):
        super().__init__('アンダーウェア1(空々神社社務所)', body=body, pantie_position=[0, 0], **options)
        self.components = io.imread('./material/k2under1_components.png') / 255
        self.components_shade = io.imread('./material/k2under1_components_shade.png')[:, :, -1] / 255

    def gen_front(self, image):
        pantie = np.array(image)
        front = np.uint8(resize(pantie[:160, :120], [1.62, 1.45])[:, 9:] * 255)
        front = np.concatenate([front[:, ::-1], front], axis=1)
        return Image.fromarray(front)

    def gen_center(self, image):
        pantie = np.array(image)
        center = np.uint8(resize(pantie[-180:-15, 546:-10], [3.9, 1.73]) * 255)[::-1, :]
        center = np.concatenate([center, center[:, ::-1]], axis=1)
        return Image.fromarray(center)

    def gen_back(self, image):
        pantie = np.array(image)
        back = np.uint8(resize(pantie[:, -100:-10], [1.73, 1.73]) * 255)[::-1, :]
        back = np.concatenate([back, back[:, ::-1]], axis=1)
        return Image.fromarray(back)

    def gen_bra(self, image):
        pantie = np.array(image)
        bra = np.uint8(resize(pantie[15:170, -200:], [4.28, 4.28]) * 255)
        return Image.fromarray(bra)

    def gen_others(self, image):
        pantie = np.array(image)
        ribbon = pantie[19:58, 5:35, :3] / 255.0
        base_color = np.mean(np.mean(ribbon[5:12, 16:20], axis=0), axis=0) * 1.2
        shade_color = np.mean(np.mean(ribbon[8:14, 7:15], axis=0), axis=0) * 1.05
        components = self.components[:, :, :3] * base_color
        shade = self.components_shade[:, :, None] * (1 - shade_color)
        components -= shade
        components = np.clip(components, 0, 1)
        components = np.dstack((components, self.components[:, :, 3]))
        return Image.fromarray(np.uint8(components * 255))

    def patch(self, image, transparent=False):
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        self.paste(patched, self.gen_front(image), [348, 158])
        self.paste(patched, self.gen_center(image), [389, 488])
        self.paste(patched, self.gen_back(image), [359, 1234])
        bra = self.gen_bra(image)
        self.paste(patched, bra, [958, 51])
        self.paste(patched, ImageOps.mirror(bra), [1132, 786])
        self.paste(patched, self.gen_others(image), [0, 0])
        return patched
