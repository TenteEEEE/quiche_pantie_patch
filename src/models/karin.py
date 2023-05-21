import os
import sys

from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.utils.imgproc import *
from src.models.class_patcher import patcher
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body="./body/body_karin.png", **options):
        super().__init__("カリン", body=body, pantie_position=[1030, 2393], **options)
        self.mask = io.imread("./mask/mask_karin.png")

        self.bra_position = [1265, 2139]
        self.bra = np.float32(io.imread("./mask/bra_karin.png") / 255)
        self.bra_shade = np.float32(io.imread("./material/bra_karin_shade.png") / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]

        self.ribbon1 = np.float32(io.imread("./material/bra_karin_ribbon1.png") / 255)
        self.ribbon1_shade = np.float32(io.imread("./material/bra_karin_ribbon1_shade.png") / 255)
        self.ribbon2 = np.float32(io.imread("./material/bra_karin_ribbon2.png") / 255)
        self.ribbon2_shade = np.float32(io.imread("./material/bra_karin_ribbon2_shade.png") / 255)
        self.ribbon3 = np.float32(io.imread("./material/bra_karin_ribbon3.png") / 255)
        self.ribbon3_shade = np.float32(io.imread("./material/bra_karin_ribbon3_shade.png") / 255)

        self.extra = np.float32(io.imread("./material/bra_karin_component1.png") / 255)
        self.extra_shade = np.float32(io.imread("./material/bra_karin_component1_shade.png") / 255)
        self.noribbon = True

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-160:-5, 548:, :])[::-1, ::-1, :]
        [pr, pc, d] = patch.shape
        pantie[105 : 105 + pr, :pc, :] = patch
        div = 49
        arrx = np.zeros(div) - 150
        arrx += np.linspace(0, 1, div) ** 2.1 * 210
        arrx += np.sin(np.linspace(0, np.pi, div)) ** 1.5 * 4
        arrx[7:17] -= np.sin(np.linspace(0, np.pi, 10)) * 6
        arry = np.linspace(0, 1, div) ** 2 * 50
        pantie = affine_transform_by_arr(pantie, arrx, arry)[:400, 7:-70]
        pantie = np.uint8(resize(pantie, [2.04, 1.85]) * 255)
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

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_shade = np.clip(bra_shade + (1 - self.bra_shade[:, :, -1])[:, :, None] ** 2.2, 0, 1)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, -1] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_texture(self, image, size):
        pantie = np.array(image)
        color, shade_color = self.extract_bra_color(pantie)
        color = np.append(shade_color * 255, 255).astype(np.uint8)
        texture = np.ones((size[0], size[1], 4), dtype=np.uint8) * color
        return Image.fromarray(texture)

    def gen_texture_by_picker(self, image, base, shade, picker):
        pantie = np.array(image)
        color, shade_color = picker(pantie)
        if base is not None:
            extra = base[:, :, :3] * color
        else:
            extra = (np.zeros_like(shade[:, :, :3]) + 1) + color
        extra_shade = (shade[:, :, -1])[:, :, None] * shade_color
        extra_shade = np.clip(extra_shade + (1 - shade[:, :, -1])[:, :, None] ** 2.2, 0, 1)
        extra = alpha_brend(extra_shade, extra, shade[:, :, -1])
        extra = np.dstack((extra, base[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(extra, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        extra = self.gen_texture(image, (150, 100))
        patched = self.paste(patched, extra, [2361, 2075])
        patched = self.paste(patched, extra, [1635, 2075])
        patched = self.paste(patched, extra, [2193, 2500])
        patched = self.paste(patched, extra, [1814, 2500])
        ribbon = self.gen_texture_by_picker(image, self.ribbon1, self.ribbon1_shade, self.extract_ribbon_color)
        patched = self.paste(patched, ribbon, [1917, 2015])
        ribbon = self.gen_texture_by_picker(image, self.ribbon2, self.ribbon2_shade, self.extract_ribbon_color)
        patched = self.paste(patched, ribbon, [1957, 2487])
        ribbon = self.gen_texture_by_picker(image, self.ribbon3, self.ribbon3_shade, self.extract_ribbon_color)
        patched = self.paste(patched, ribbon, [2745, 2038])
        patched = self.paste(patched, ImageOps.mirror(ribbon), [1058, 2038])
        extra = self.gen_texture_by_picker(image, self.extra, self.extra_shade, self.extract_bra_color)
        patched = self.paste(patched, extra, [1078, 1882])
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        return patched
