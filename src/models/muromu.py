import os
import sys

current_directory = os.getcwd()
sys.path.append(os.getcwd())
from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.utils.imgproc import *
from src.models.class_patcher import patcher
from skimage.color import rgb2hsv, hsv2rgb
from skimage import restoration


class patcher(patcher):
    def __init__(self, body="./body/body_muromu.png", **options):
        super().__init__("むろむ", body=body, pantie_position=[12, 82], **options)
        self.mask = io.imread("./mask/mask_muromu.png")
        self.bra_position = [1262, 891]
        self.bra = np.float32(io.imread("./mask/bra_muromu.png") / 255)
        self.bra_center = np.float32(io.imread("./mask/bra_muromu_center.png") / 255)
        self.bra_shade = np.float32(io.imread("./material/bra_muromu_shade.png") / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]

        self.extra1_position = [65, 277]
        self.extra1_shade = np.float32(io.imread("./material/bra_muromu_component_shade.png") / 255)
        self.extra1 = np.zeros_like(self.extra1_shade) + 1.0

        self.ribbon_position = [1585, 653]
        self.ribbon = np.float32(io.imread("./material/muromu_ribbon.png") / 255)
        self.ribbon_shade = np.float32(io.imread("./material/muromu_ribbon_shade.png") / 255)[:, :, -1]

        self.noribbon = True

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:300, :300, :]
        back = pantie[:-7, 250:, :][::-1, ::-1]

        arrx = np.zeros(9) - 100
        arrx += np.linspace(0, 1, 9) ** 2 * 64
        arrx[2] -= 1
        arrx[3] -= 2
        arry = np.zeros(9)
        arry[1] = -18
        arry[2] = -36
        arry[3] = -18
        front = affine_transform_by_arr2(front, arrx, arry)[40:245]
        front = np.uint8(front * 255)

        arrx = np.zeros(7)
        arrx = np.linspace(0, 1, 7) ** 3 * 10
        arry = np.linspace(0, 1, 7) * 28
        back = affine_linear_transform_by_arr(back, arrx, arry)[:-10, :-35]
        back = np.uint8(back * 255)

        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        pantie = np.zeros((fr + br, np.max([fc, bc]), 4), dtype=np.uint8)
        pantie[:fr, :fc, :] = front
        pantie[fr:, :bc, :] = back
        pantie = resize(pantie, [3.1, 3.1])[:, 50:]
        pantie = np.uint8(pantie * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
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

    def extract_ribbon_color(self, pantie):
        ribbon = pantie[-8:, :12, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        ribbon_shade = pantie[-4:, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)
        ribbon_shade_color = rgb2hsv(ribbon_shade_color[None, None])
        ribbon_shade_color[0, 0, 1] *= ribbon_shade_color[0, 0, 2] / 0.3
        if ribbon_shade_color[0, 0, 1] > 0.7:
            ribbon_shade_color[0, 0, 1] *= 0.7
        ribbon_shade_color[0, 0, 2] *= ribbon_shade_color[0, 0, 2] / 0.4
        ribbon_shade_color = np.clip(hsv2rgb(ribbon_shade_color)[0, 0], 0, 1)
        return ribbon_color, ribbon_shade_color

    def gen_bra_color_texture(self, image, base, shade):
        pantie = np.array(image)
        color, shade_color = self.extract_bra_color(pantie)
        extra = base[:, :, :3] * color
        extra_shade = (shade[:, :, -1])[:, :, None] * shade_color
        extra_shade = np.clip(extra_shade + (1 - shade[:, :, -1])[:, :, None] ** 2.2, 0, 1)  # simple gamma correction
        extra = alpha_brend(extra_shade, extra, shade[:, :, -1])
        extra = np.dstack((extra, base[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(extra, 0, 1) * 255))

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [3.2, 3.2])
        bra_center = np.copy(self.bra_center)
        bra_center[10 : 10 + center.shape[0], 80 : 80 + center.shape[1], :3] = center * np.float32(
            bra_center[10 : 10 + center.shape[0], 80 : 80 + center.shape[1], :3] > 0
        )
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_shade = np.clip(
            bra_shade + (1 - self.bra_shade[:, :, -1])[:, :, None] ** 2.2, 0, 1
        )  # simple gamma correction
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))

        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_ribbon(self, image):
        pantie = np.array(image)
        ribbon_color, ribbon_shade_color = self.extract_ribbon_color(pantie)
        ribbon = self.ribbon[:, :, :3] * ribbon_color
        ribbon_shade = self.ribbon_shade[:, :, None] * ribbon_shade_color
        ribbon = alpha_brend(ribbon_shade, ribbon, self.ribbon_shade)
        ribbon = np.dstack((ribbon, self.ribbon[:, :, -1] > 0.5))
        return Image.fromarray(np.uint8(ribbon * 255))

    def gen_extra(self, image):
        return self.gen_bra_color_texture(image, self.extra1, self.extra1_shade)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (2048, 2048))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.gen_extra(image), self.extra1_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        patched = self.paste(patched, self.gen_ribbon(image), self.ribbon_position)
        return patched
