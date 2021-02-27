from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_koyuki.png', **options):
        super().__init__('狐雪', body=body, pantie_position=[3279, 344], **options)
        self.mask = io.imread('./mask/mask_koyuki.png')

        self.bra_position = [2546, 0]
        self.bra = np.float32(io.imread('./mask/bra_koyuki.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_koyuki_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_koyuki_shade.png') / 255)
        self.bra_lace = np.float32(io.imread('./material/bra_koyuki_lace.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]
        self.bra_lace_mask = self.bra_lace[:, :, -1] > 0.7

        self.extra_position = [3569, 284]
        self.extra = np.float32(io.imread('./material/koyuki_extra.png') / 255)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_bra(self, image):
        pantie = np.array(image)

        # pickup colors
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
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)

        # making a center texture
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [1.8, 1.8])

        bra_center = np.copy(self.bra_center)
        bra_center[20:20 + center.shape[0], 800:800 + center.shape[1], :3] = center * np.float32(bra_center[20:20 + center.shape[0], 800:800 + center.shape[1], :3] > 0)
        bra_center[20:20 + center.shape[0], 410:410 + center.shape[1], :3] = center[:, ::-1] * np.float32(bra_center[20:20 + center.shape[0], 410:410 + center.shape[1], :3] > 0)

        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_lace = self.bra_lace[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_lace, bra, self.bra_lace_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_extra(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        extra = self.extra[:, :, :3] * ribbon_color
        extra = np.dstack((extra, self.extra[:, :, -1]))
        return Image.fromarray(np.uint8(np.clip(extra, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)
        pantie = ribbon_inpaint(pantie)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch
        pantie[-140:, 546:, :] = 0
        front = pantie[:, :300]
        arrx = np.linspace(0, 1, 25) * 100 - 60
        arry = np.linspace(0, 1, 25)**2 * 170
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(resize(front[:310, :230], [1.4, 1.3]) * 255)
        front = np.rot90(front, -1)[:, 112:]

        back = pantie[:, 300:][:, ::-1]
        arrx = np.linspace(0, 1, 49)**2 * 360 - 150
        arry = np.linspace(0, 1, 49)**2 * 170
        back_r = np.rot90(affine_transform_by_arr(back, arrx, arry)[::-1], -1)[:250]
        arrx = np.linspace(0, 1, 49)**2 * 345 - 150
        back_l = np.rot90(affine_transform_by_arr(back, arrx, arry)[::-1], -1)[:250]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 80
        back_r = affine_transform_by_arr(back_r, arrx, arry)
        back_r = np.uint8(resize(back_r[:200, :340], [1.3, 1.45]) * 255)
        back_r = back_r[:, :-5]
        back_l = affine_transform_by_arr(back_l, arrx, arry)
        back_l = np.uint8(resize(back_l[:200, :340], [1.3, 1.45]) * 255)
        back_l = back_l[::-1, :-5]

        [fr, fc, d] = front.shape
        [br, bc, d] = back_r.shape
        pantie = np.zeros((np.max([fr, br]), fc + bc, d), dtype=np.uint8)
        pantie[:br, :bc] = back_r
        pantie[:fr, bc:] = front
        pantie = pantie[9:]
        pantie = np.concatenate([pantie[::-1], pantie], axis=0)
        pantie[fr - br:fr - 9, :bc] = back_l[:-9]
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        patched = self.paste(patched, self.gen_extra(image), self.extra_position)
        return patched
