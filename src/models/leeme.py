import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_leeme.png', **options):
        super().__init__('リーメ(下着)', body=body, pantie_position=[-9, 475], **options)
        self.mask = io.imread('./mask/mask_leeme.png')
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [1146, 721]
            self.bra = np.float32(io.imread('./mask/bra_leeme.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_leeme_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_leeme_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_leeme_frill.png') / 255)
            self.bra_alpha = self.bra[:, :, 0] > 0
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_frill_mask = self.bra_frill[:, :, -1] > 0.5
            self.components = np.float32(io.imread('./material/components_leeme.png') / 255)
            self.components_shade = np.float32(io.imread('./material/components_leeme_shade.png') / 255)
            self.hook = Image.open('./material/hook_leeme.png')

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:116, :260]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 15
        front = affine_transform_by_arr(front, arrx, arry)[:-1, :]

        back = pantie[:-8, 260:][::-1, ::-1]
        arry = np.linspace(0, 1, 25)**2 * 15
        back = affine_transform_by_arr(back, arrx, arry)[1:, :]

        front = np.pad(front, [(0, 0), (0, back.shape[1] - front.shape[1]), (0, 0)], mode='constant')
        pantie = np.concatenate((front, back), axis=0)
        pantie = np.uint8(resize(pantie, [2.87, 2.862]) * 255)[:, 20:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)

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
        center = resize(center, [3.2, 3.2])

        # painting colors
        # bra_center = np.float32(io.imread('./mask/bra_leeme_center.png')/255)
        bra_center = np.copy(self.bra_center)
        bra_center[70:70 + center.shape[0], 90:90 + center.shape[1], :3] = center * np.float32(bra_center[70:70 + center.shape[0], 90:90 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_frill = self.bra_frill[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_frill, bra, self.bra_frill_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra_alpha))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_components(self, image):
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

        components = np.copy(self.components)
        components = self.components[:, :, :3] * front_color
        components_shade = (self.components_shade[:, :, -1])[:, :, None] * front_shade_color

        # overlaying layers
        components = alpha_brend(components_shade, components, self.components_shade[:, :, -1])
        components = np.dstack((components, self.components[:, :, -1]))
        return Image.fromarray(np.uint8(np.clip(components, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.with_bra:
            bra = self.gen_bra(image)
            patched = self.paste(patched, bra, self.bra_position)
            patched = self.paste(patched, ImageOps.mirror(bra), (self.body_size[0] - self.bra_position[0] - bra.size[0], self.bra_position[1]))
            patched = self.paste(patched, self.gen_components(image), (0, 0))
            patched = self.paste(patched, self.hook, (1621, 1336))
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
