import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_cc0.png', **options):
        super().__init__('cc0', body=body, pantie_position=[407, 838], **options)
        try:
            self.is_4k = self.options['is_4k']
        except:
            self.is_4k = self.ask(question='4K(4096x4096) resolution texture?', default=False)
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=False)
        if self.with_bra:
            self.bra_position = [1023, 0]
            self.bra = np.float32(io.imread('./mask/bra_orion.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_orion_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_orion_shade.png') / 255)
            self.bra_component = np.float32(io.imread('./material/bra_orion_component.png') / 255)
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_component_mask = self.bra_component[:, :, -1] > 0.5

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def convert(self, image):
        pantie = np.array(image)
        arrx = np.zeros(100)
        arry = np.zeros(100)
        arry[5:45] -= np.sin(np.linspace(0, 1 * np.pi, 40)) * 50
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie = pantie[:, 11:]
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        pantie = np.uint8(pantie * 255)
        return Image.fromarray(pantie)

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
        center = resize(center, [2.42, 2.42])

        bra_center = np.copy(self.bra_center)
        bra_center[225:225 + center.shape[0], 25:25 + center.shape[1], :3] = center * np.float32(bra_center[225:225 + center.shape[0], 25:25 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_component = self.bra_component[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_component, bra, self.bra_component_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            if self.is_4k:
                patched = Image.new("RGBA", (4096, 4096))
            else:
                patched = Image.new("RGBA", (2048, 2048))
        else:
            patched = self.body.copy()
        if not self.is_4k or patched.size[0] < 2048:
            pantie_position = self.pantie_position
        else:
            pantie_position = (int(self.pantie_position[0] * 2), int(self.pantie_position[1] * 2))
            pantie = pantie.resize((int(pantie.width * 2), int(pantie.height * 2)), resample=Image.BICUBIC)
        patched = self.paste(patched, pantie, pantie_position)
        if self.with_bra:
            bra = self.gen_bra(image)
            if not self.is_4k or patched.size[0] < 2048:
                bra_position = self.bra_position
            else:
                bra_position = (int(self.bra_position[0] * 2), int(self.bra_position[1] * 2))
                bra = bra.resize((int(bra.width * 2), int(bra.height * 2)), resample=Image.BICUBIC)
            patched = self.paste(patched, bra, bra_position)
            patched = self.paste(patched, ImageOps.mirror(bra), [bra_position[0] - bra.width, bra_position[1]])
        return patched
