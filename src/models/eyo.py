from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_eyo.png', **options):
        super().__init__('イヨ', body=body, pantie_position=[1423, 877], **options)
        self.mask = io.imread('./mask/mask_eyo.png')
        self.bra_position = [298, 1301]
        try:
            self.use_ribbon_mesh = self.options['use_ribbon_mesh']
        except:
            self.use_ribbon_mesh = self.ask(question='Use ribbon mesh?', default=True)

        self.bra_position = [1141, 57]
        self.bra = np.float32(io.imread('./mask/bra_eyo.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_eyo_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_eyo_shade_1.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]

        self.extra_position = [1928, 30]
        self.extra_shade = np.float32(io.imread('./material/bra_eyo_shade_2.png') / 255)
        self.extra = np.zeros_like(self.extra_shade) + 1.

        if self.use_ribbon_mesh:
            self.ribbon_position = [1569, 1288]
            self.ribbon = np.float32(io.imread('./material/eyo_ribbon.png') / 255)
            self.ribbon_shade = np.float32(io.imread('./material/eyo_ribbon_shade.png') / 255)[:, :, -1]

    def convert(self, image):
        pantie = np.array(image)
        if self.use_ribbon_mesh:
            pantie = ribbon_inpaint(pantie)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = patch[::-1, ::-1]
        front = pantie[:200, :264 + 40]
        back = pantie[:-8, 264 - 40:][:, ::-1]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 170
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(resize(front, [1.95, 1.95]) * 255)
        arry = np.linspace(0, 1, 25)**2 * 230
        back = affine_transform_by_arr(back, arrx, arry)[:, :-100]
        back = np.uint8(resize(back, [1.95, 1.95]) * 255)[::-1]
        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shifty = 80
        pantie = np.zeros((fr + br - shifty, np.max([fc, bc]), d), dtype=np.uint8)
        pantie[:fr, :fc] = front
        pantie[fr:, :bc] = back[shifty:]
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def extract_bra_color(self, pantie):
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
        return front_color, front_shade_color

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [3.7, 3.7])
        bra_center = np.float32(io.imread('./mask/bra_eyo_center.png') / 255)
        bra_center[:center.shape[0], 55:55 + center.shape[1], :3] = center * np.float32(bra_center[:center.shape[0], 55:55 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_extra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        extra = self.extra[:, :, :3] * front_color
        extra_shade = (self.extra_shade[:, :, -1])[:, :, None] * front_shade_color
        extra = alpha_brend(extra_shade, extra, self.extra_shade[:, :, -1])
        extra = np.dstack((extra, self.extra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(extra, 0, 1) * 255))

    def gen_ribbon(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)
        ribbon_shade_color = rgb2hsv(ribbon_shade_color[None, None])
        ribbon_shade_color[0, 0, 1] *= ribbon_shade_color[0, 0, 2] / 0.3
        if ribbon_shade_color[0, 0, 1] > 0.7:
            ribbon_shade_color[0, 0, 1] *= 0.7
        ribbon_shade_color[0, 0, 2] *= ribbon_shade_color[0, 0, 2] / 0.4
        ribbon_shade_color = np.clip(hsv2rgb(ribbon_shade_color)[0, 0], 0, 1)
        ribbon = self.ribbon[:, :, :3] * ribbon_color
        ribbon_shade = self.ribbon_shade[:, :, None] * ribbon_shade_color
        ribbon = alpha_brend(ribbon_shade, ribbon, self.ribbon_shade)
        ribbon = np.dstack((ribbon, self.ribbon[:, :, -1] > 0.5))
        return Image.fromarray(np.uint8(ribbon * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (2048, 2048))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        patched = self.paste(patched, self.gen_extra(image), self.extra_position)
        if self.use_ribbon_mesh:
            patched = self.paste(patched, self.gen_ribbon(image), self.ribbon_position)
        return patched
