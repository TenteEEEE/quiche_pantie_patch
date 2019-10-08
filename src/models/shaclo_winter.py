import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_shaclo_winter.png', **options):
        super().__init__('シャーロ(冬服)', body=body, pantie_position=[3111, 60], **options)
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [3290, 8]
            self.bra = np.float32(io.imread('./mask/bra_shaclo_winter.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_shaclo_winter_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_shaclo_winter_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_shaclo_winter_frill.png') / 255)
            self.bra_lace = np.float32(io.imread('./material/bra_shaclo_winter_lace.png') / 255)
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_lace_mask = self.bra_lace[:, :, -1] > 0
            self.bra_frill_mask = self.bra_frill[:, :, -1] > 0

    def gen_bra(self, image):
        def pick_color(arr):
            return np.mean(np.mean(arr, axis=0), axis=0)

        def alpha_brend(img1, img2, mask):
            return img1 * mask[:, :, None] + img2 * (1 - mask)[:, :, None]
        pantie = np.array(image)
        
        # pickup colors
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = pick_color(front)
        front_shade_color = pick_color(front_shade)
        front_shade_color = rgb2hsv(front_shade_color[None,None])
        front_shade_color[0,0,1] *= front_shade_color[0,0,2]/0.3
        if front_shade_color[0,0,1]>0.7:
            front_shade_color *= 0.8
        front_shade_color[0,0,2] *= front_shade_color[0,0,2]/0.2
        front_shade_color = np.clip(hsv2rgb(front_shade_color)[0,0],0,1)
        # ribbon = pantie[24:32, 15:27, :3]/255.0
        # ribbon_color = pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = pick_color(ribbon_shade)

        # making a center texture
        center = pantie[20:170, -200:-15, :3]
        center = np.rot90(center[::-1, ::-1])
        center = resize(center, [3.5, 3.5])
        
        # painting colors
        center_mask = np.uint8(self.bra_center[20:20 + center.shape[0], -center.shape[1] - 10:-10, 0] > 0)
        bra_frill = self.bra_frill[:, :, :3] * ribbon_shade_color
        bra_center = np.copy(self.bra_center)
        bra_center[20:20 + center.shape[0], -center.shape[1] - 10:-10, :3] = center * center_mask[:, :, None]
        bra = self.bra[:, :, :3] * front_color
        bra_lace = self.bra_lace[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        
        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0)
        bra = alpha_brend(bra_lace, bra, self.bra_lace_mask)
        bra = alpha_brend(bra_frill, bra, self.bra_frill_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, bra[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)

        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-190:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 50), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[142:142 + pr, :pc, :] = np.uint8(patch * 255)

        arrx = np.zeros(100)
        arry = np.zeros(100)
        arrx[12:62] += np.sin(np.linspace(0, np.pi, 50)) * 25
        arrx[58:83] += np.sin(np.linspace(0, np.pi, 25)) * 14
        arrx -= 50
        pantie = affine_transform_by_arr(pantie, arrx, arry, smoothx=True)
        pantie = np.rot90(pantie, -1)[:, ::-1]
        pantie = np.uint8(resize(pantie, [1.66, 1.66]) * 255)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.with_bra:
            bra = self.gen_bra(image)
            patched = self.paste(patched, bra, self.bra_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
