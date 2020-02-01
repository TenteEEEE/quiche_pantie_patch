import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_supica.png', **options):
        super().__init__('スピカ', body=body, pantie_position=[19, 0], **options)
        self.mask = io.imread('./mask/mask_supica.png')
        self.components = io.imread('./material/supica_components.png')[:, :, -1] / 255.0
        self.components_shade = io.imread('./material/supica_components_shade.png')[:, :, -1] / 255.0
        self.components_position = [1221, 17]

    def gen_components(self, image):
        pantie = np.array(image)
        ribbon = pantie[19:58, 5:35, :3] / 255.0
        base_color = np.mean(np.mean(ribbon[5:12, 16:20], axis=0), axis=0)
        shade_color = np.mean(np.mean(ribbon[8:14, 7:15], axis=0), axis=0)
        components = self.components[:, :, None] * base_color
        shade = self.components_shade[:, :, None] * (1 - shade_color)
        components -= shade
        components = np.dstack((components, components[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(components, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-150:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 50), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[142:142 + pr, :pc, :] = np.uint8(patch * 255)
        pantie = np.uint8(resize(pantie, [1.38, 1.62]) * 255)[:, 11:]
        pantie = np.bitwise_and(pantie, self.mask)[:, 1:]
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        components = self.gen_components(image)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        components = self.gen_components(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        self.paste(patched, pantie, self.pantie_position)
        self.paste(patched, components, self.components_position)
        self.paste(patched, ImageOps.mirror(components), [2048 - self.components_position[0] - components.width, self.components_position[1]])
        return patched
