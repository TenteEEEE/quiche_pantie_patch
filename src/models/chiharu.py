import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_chiharu.png', **options):
        super().__init__('東狐千春', body=body, pantie_position=[1038, 2930], **options)
        self.mask = io.imread('./mask/mask_chiharu.png')
        self.ribbon_base = io.imread('./material/chiharu_pantie_ribbon.png') / 255
        self.ribbon_shade = io.imread('./material/chiharu_pantie_ribbon_shade.png')[:, :, 3] / 255
        self.ribbon_alpha = self.ribbon_base[:, :, -1]
        self.ribbon_base = self.ribbon_base[:, :, :3]
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [1871, 2358]
            self.bra_base = np.float32(io.imread('./material/bra_chiharu_base.png') / 255)
            self.bra_center = io.imread('./mask/bra_chiharu_center.png')
            self.bra_shade = np.float32(io.imread('./material/bra_chiharu_shade.png')[:, :, -1] / 255)
            self.bra_alpha = self.bra_base[:, :, 3]

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_bra(self, image):
        pantie = np.array(image)
        ribbon = pantie[19:58, 5:35, :3]
        bra = np.zeros(self.bra_base.shape, dtype=np.uint8)

        base_color = self.pick_color(ribbon[5:12, 16:20]) / 255
        shade_color = self.pick_color(ribbon[8:14, 7:15]) / 255
        bra_base = (self.bra_base[:, :, :3] > 0) * base_color
        bra_shade = self.bra_shade[:, :, None] * (1 - shade_color)
        bra_frame = bra_base - bra_shade
        bra_frame = np.dstack((bra_frame, self.bra_alpha))
        bra_frame = np.clip(bra_frame, 0, 1)

        center = np.rot90(pantie[:, ::-1, :3], 1)[400:, 15:170]
        center = np.bitwise_and(center, self.bra_center[560:560 + center.shape[0], 110:110 + center.shape[1], :3])
        center = np.dstack((center, self.bra_center[560:560 + center.shape[0], 110:110 + center.shape[1], 0]))

        bra[560:560 + center.shape[0], 110:110 + center.shape[1]] = center
        bra = alpha_brend(bra_frame, np.float32(bra / 255), self.bra_alpha)
        return Image.fromarray(np.uint8(bra * 255))

    def convert(self, image):
        pantie = np.array(image)
        ribbon = pantie[19:58, 5:35, :3]

        patch = np.copy(pantie[-120:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[130:130 + pr, :pc, :] = patch[::-1, ::-1]
        pantie = np.uint8(resize(pantie[:280, ::-1], [1.25, 1.25]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)

        base_color = self.pick_color(ribbon[5:12, 16:20]) / 255
        shade_color = self.pick_color(ribbon[8:14, 7:15]) / 255
        ribbon_base = (self.ribbon_base > 0) * base_color
        ribbon_shade = self.ribbon_shade[:, :, None] * (1 - shade_color)
        ribbon = ribbon_base - ribbon_shade
        ribbon = np.dstack((ribbon, self.ribbon_alpha > 0))
        ribbon = np.clip(ribbon, 0, 1)
        pantie = alpha_brend(ribbon, np.float32(pantie / 255), self.ribbon_alpha)
        return Image.fromarray(np.uint8(pantie * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        if self.with_bra:
            bra = self.gen_bra(image)
            patched = self.paste(patched, bra, self.bra_position)
        return patched
