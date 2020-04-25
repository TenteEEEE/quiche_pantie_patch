import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_k2maid1.png', **options):
        super().__init__('メイド服1(空々神社社務所)', body=body, pantie_position=[2932, 3298], **options)
        self.mask = io.imread('./mask/mask_k2maid1.png')

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:116, :150]
        back = pantie[:-8, -150:][::-1, ::-1]
        pantie = np.concatenate((front, back), axis=0)
        pantie = np.uint8(resize(pantie, [1.14, 1]) * 255)[:, 7:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)

    def gen_texture(self, image, size):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3]
        front_color = np.mean(np.mean(front, axis=0), axis=0)
        front_color = np.append(front_color, 255).astype(np.uint8)
        texture = np.ones((size[0], size[1], 4),  dtype=np.uint8) * front_color
        return Image.fromarray(texture)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_texture(image, (40, 1840)),  [2165, 3940])
        return patched
