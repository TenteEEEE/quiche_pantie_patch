from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.utils.imgproc import *
from src.models.class_patcher import patcher
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body="./body/body_falmna.png", **options):
        super().__init__("ファルムナ", body=body, pantie_position=[2962, 1128], **options)
        self.mask = io.imread("./mask/mask_falmna.png")
        self.mask_inter = io.imread("./mask/mask_falmna_inter.png")

        self.bra_position = [3494, 808]
        self.bra = np.float32(io.imread("./mask/bra_falmna.png") / 255)
        self.bra_center = np.float32(io.imread("./mask/bra_falmna_center.png") / 255)
        self.bra_shade = np.float32(io.imread("./material/bra_falmna_shade.png") / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]

        self.extra1_position = [3046, 1245]
        self.extra1_shade = np.float32(io.imread("./material/falmna_extra1.png") / 255)
        self.extra1 = np.zeros_like(self.extra1_shade) + 1.0

        self.extra2_position = [3977, 973]
        self.extra2_shade = np.float32(io.imread("./material/falmna_extra2.png") / 255)
        self.extra2 = np.zeros_like(self.extra2_shade) + 1.0

        self.extra3_position = [3737, 975]
        self.extra3 = Image.open("./material/falmna_extra3.png")

        self.ribbon_position1 = [3232, 1402]
        self.ribbon_position2 = [3606, 1013]
        self.ribbon = np.float32(io.imread("./material/falmna_ribbon.png") / 255)
        self.ribbon_shade = np.float32(io.imread("./material/falmna_ribbon_shade.png") / 255)[:, :, -1]

    def convert(self, image):
        pantie = np.array(image)
        # pantie = ribbon_inpaint(pantie)
        front = pantie[:200, : 280 + 40]
        inter = pantie[:50, 120:280]
        back = pantie[:-8, 280 - 40 :]  # [:, ::-1]
        inter = np.uint8(resize(inter, [1.38, 1.74]) * 255)
        inter = np.bitwise_and(inter, self.mask_inter)
        arrx = np.zeros(6)
        arry = np.linspace(0, 1, 6) ** 1.5 * -200
        front = affine_linear_transform_by_arr(front, arrx, arry)
        front = np.uint8(resize(front, [1.38, 1.25]) * 255)[:213, 13:200]
        arrx = np.linspace(0, 1, 6) ** 0.8 * 95
        arry = np.zeros(6)
        back = affine_linear_transform_by_arr(back, arrx, arry)[:318]
        back = np.uint8(resize(back, [1.382, 1.25]) * 255)[::-1, ::-1][:, 13:-20]
        [fr, fc, d] = front.shape
        [ir, ic, d] = inter.shape
        [br, bc, d] = back.shape
        shifty = 0
        pantie = np.zeros((fr + br - shifty, np.max([fc, bc]), d), dtype=np.uint8)
        pantie[:fr, :fc] = front
        pantie[fr:, :bc] = back
        pantie = np.bitwise_and(pantie, self.mask[:-1, 1:])
        pantie[pantie[:, :, -1] == 0] = 0
        dx = 150
        pantie[:ir, dx : dx + ic, :3] += np.bitwise_or(pantie[:ir, dx : dx + ic, -1][:, :, None] == 0, inter[:, :, :3])
        pantie[:ir, dx : dx + ic, -1] = np.bitwise_or(pantie[:ir, dx : dx + ic, -1], inter[:, :, -1])
        pantie = np.hstack([pantie[:, ::-1], pantie])

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
        return ribbon_color, ribbon_shade_color

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [2.0, 2.0])
        bra_center = np.copy(self.bra_center)
        bra_center[390 : 390 + center.shape[0], : center.shape[1], :3] = center * np.float32(
            bra_center[390 : 390 + center.shape[0], : center.shape[1], :3] > 0
        )
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))

        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_ribbon_color_texture(self, image, base, shade):
        pantie = np.array(image)
        ribbon_color, ribbon_shade_color = self.extract_ribbon_color(pantie)
        extra = base[:, :, :3] * ribbon_color
        extra_shade = (shade[:, :, -1])[:, :, None] * ribbon_shade_color
        extra = alpha_brend(extra_shade, extra, shade[:, :, -1])
        extra = np.dstack((extra, base[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(extra, 0, 1) * 255))

    def gen_extra1(self, image):
        return self.gen_ribbon_color_texture(image, self.extra1, self.extra1_shade)

    def gen_extra2(self, image):
        return self.gen_ribbon_color_texture(image, self.extra2, self.extra2_shade)

    def gen_ribbon(self, image):
        pantie = np.array(image)
        ribbon_color, ribbon_shade_color = self.extract_ribbon_color(pantie)
        ribbon = self.ribbon[:, :, :3] * ribbon_color
        ribbon_shade = self.ribbon_shade[:, :, None] * ribbon_shade_color
        ribbon = alpha_brend(ribbon_shade, ribbon, self.ribbon_shade)
        ribbon = np.dstack((ribbon, self.ribbon[:, :, -1] > 0.5))
        return Image.fromarray(np.uint8(ribbon * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        patched = self.paste(patched, self.gen_extra1(image), self.extra1_position)
        patched = self.paste(patched, self.gen_extra2(image), self.extra2_position)
        patched = self.paste(patched, self.extra3, self.extra3_position)
        ribbon = self.gen_ribbon(image)
        patched = self.paste(patched, ribbon, self.ribbon_position1)
        patched = self.paste(patched, ribbon, self.ribbon_position2)
        return patched
