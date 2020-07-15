import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_rei.png', **options):
        super().__init__('零', body=body, pantie_position=[0, 0], **options)
        self.pantie_ribbon_alpha = np.float32(io.imread('./material/rei_pantie_ribbon.png')[:, :, -1] / 255)
        self.pantie_ribbon_shade_alpha = np.float32(io.imread('./material/rei_pantie_ribbon_shade.png')[:, :, -1] / 255)
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_center = io.imread('./material/rei_bra_center.png')
            self.bra_center_deco = np.float32(io.imread('./material/rei_bra_center_deco.png') / 255)
            self.bra_center_shade_alpha = np.float32(io.imread('./material/rei_bra_center_shade.png')[:, :, -1] / 255)
            self.bra_others_alpha = np.float32(io.imread('./material/rei_bra_others.png')[:, :, -1] / 255)
            self.bra_others_shade_alpha = np.float32(io.imread('./material/rei_bra_others_shade.png')[:, :, -1] / 255)
            self.bra_ribbon_alpha = np.float32(io.imread('./material/rei_bra_ribbon.png')[:, :, -1] / 255)
            self.bra_ribbon_shade_alpha = np.float32(io.imread('./material/rei_bra_ribbon_shade.png')[:, :, -1] / 255)

    def convert_front(self, image):
        pantie = np.array(image)
        front = pantie[:100, :300]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 150
        front = affine_transform_by_arr(front, arrx, arry)[:, :225]
        front = np.uint8(resize(front, [0.75, 0.75]) * 255)[:, 4:]
        front = np.concatenate([front[:, ::-1], front], axis=1)
        return Image.fromarray(front)

    def convert_back(self, image):
        pantie = np.array(image)
        back = pantie[:250, 300:][:, ::-1]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 150
        back = affine_transform_by_arr(back, arrx, arry)[:, :260]
        back = np.rot90(back, -1)
        arrx = np.zeros(25)
        arry = np.linspace(1, 0, 25)**3 * -240
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(resize(np.rot90(back), [0.75, 0.75]) * 255)[:, 9:]
        back = np.concatenate([back[:, ::-1], back], axis=1)
        return Image.fromarray(back)

    def convert_bottom(self, image):
        pantie = np.array(image)
        bottom = np.rot90(pantie[-170:-14, 550:, :])
        bottom = np.concatenate((bottom, bottom[::-1]), axis=0)
        bottom = np.uint8(resize(bottom, [0.58, .91]) * 255)
        return Image.fromarray(bottom)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def vivid_color(self, color):
        color = rgb2hsv(color[None, None])
        color[0, 0, 1] *= color[0, 0, 2] / 0.3
        if color[0, 0, 1] > 0.7:
            color[0, 0, 1] *= 0.7
        color[0, 0, 2] *= color[0, 0, 2] / 0.4
        color = np.clip(hsv2rgb(color)[0, 0], 0, 1)
        return color

    def gen_bra_center(self, image):
        pantie = np.array(image)
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_shade_color = self.pick_color(front_shade)
        front_shade_color = self.vivid_color(front_shade_color)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)

        bra_center = np.copy(self.bra_center)
        center = pantie[20:153, -200:-15, :3]
        bra_center[:, :center.shape[1], :3] = center
        bra_center[:, -center.shape[1]:, :3] = center[:, ::-1]
        bra_center = np.float32(bra_center / 255)
        bra_deco = np.copy(self.bra_center_deco)
        bra_deco_alpha = bra_deco[:, :, -1]
        bra_deco = bra_deco[:, :, :3] * ribbon_color
        bra_shade = np.copy(self.bra_center_shade_alpha)
        shade = bra_shade[:, :, None] * front_shade_color

        out = alpha_brend(bra_center[:, :, :3], bra_deco, 1 - bra_deco_alpha)
        out = alpha_brend(out, shade, 1 - bra_shade)
        out = np.dstack((out, bra_center[:, :, -1]))
        out = np.uint8(np.clip(out, 0, 1) * 255)
        return Image.fromarray(out)

    def gen_bra_others(self, image):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        front_shade_color = self.vivid_color(front_shade_color)

        others_alpha = np.copy(self.bra_others_alpha)
        shade_alpha = np.copy(self.bra_others_shade_alpha)
        others = others_alpha[:, :, None] * front_color
        shade = shade_alpha[:, :, None] * front_shade_color
        out = alpha_brend(others, shade, 1 - shade_alpha)
        out = np.dstack((out, others_alpha))
        out = np.uint8(np.clip(out, 0, 1) * 255)
        return Image.fromarray(out)

    def paint_ribbon_color(self, image, base_alpha, shade_alpha):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)
        ribbon_shade_color = self.vivid_color(ribbon_shade_color)

        base = base_alpha[:, :, None] * ribbon_color
        shade = shade_alpha[:, :, None] * ribbon_shade_color
        out = alpha_brend(base, shade, 1 - shade_alpha)
        out = np.dstack((out, base_alpha))
        out = np.uint8(np.clip(out, 0, 1) * 255)
        return Image.fromarray(out)

    def gen_pantie_ribbon(self, image):
        return self.paint_ribbon_color(image, self.pantie_ribbon_alpha, self.pantie_ribbon_shade_alpha)

    def gen_bra_ribbon(self, image):
        return self.paint_ribbon_color(image, self.bra_ribbon_alpha, self.bra_ribbon_shade_alpha)

    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.convert_back(image), [329, 680])
        patched = self.paste(patched, self.convert_front(image), [326, 801])
        patched = self.paste(patched, self.convert_bottom(image), [666, 802])
        patched = self.paste(patched, self.gen_pantie_ribbon(image), [232, 808])
        if self.with_bra:
            patched = self.paste(patched, self.gen_bra_center(image), [287, 853])
            patched = self.paste(patched, self.gen_bra_others(image), [-1, 2])
            patched = self.paste(patched, self.gen_bra_ribbon(image), [34, 899])
        return patched
