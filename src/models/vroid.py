import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_vroid.png', **options):
        super().__init__('VRoid', body=body, pantie_position=[482, 944], **options)
        self.mask = io.imread('./mask/mask_vroid.png')
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [493, 197]
            self.bra = np.float32(io.imread('./mask/bra_vroid.png') / 255)
            self.bra_alpha = np.float32(io.imread('./material/bra_vroid_alpha.png')[:, :, -1] / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_vroid_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_vroid_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_vroid_frill.png') / 255)
            self.bra_ribbon = np.float32(io.imread('./material/bra_vroid_ribbon.png') / 255)
            self.bra_ribbon_shade = np.float32(io.imread('./material/bra_vroid_ribbon_shade.png') / 255)
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_ribbon_mask = self.bra_ribbon[:, :, -1] > 0.5
            self.bra_frill_mask = self.bra_frill[:, :, -1] > 0.5

    def convert(self, image):
        pantie = np.array(image)

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (180, 40), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[157:157 + pr, :pc, :] = np.uint8(patch * 255)

        # Affine transform matrix
        pantie = np.pad(pantie, [(100, 0), (10, 0), (0, 0)], mode='constant')
        arrx = np.zeros(100)
        arrx[10:50] = (np.sin(np.linspace(0, 1 * np.pi, 100))[20:60] * 30)
        arrx[50:] = -(np.sin(np.linspace(0, 1 * np.pi, 100))[50:] * 15)
        arrx[40:60] += (np.sin(np.linspace(0, 1 * np.pi, 100))[40:60] * 15)
        arrx[00:10] -= (np.sin(np.linspace(0, 1 * np.pi, 100))[50:60] * 35)
        arry = (np.sin(np.linspace(0, 0.5 * np.pi, 100)) * 70)
        arry[10:30] -= (np.sin(np.linspace(0, 1 * np.pi, 100)) * 20)[50:70]
        pantie = affine_transform_by_arr(pantie, arrx, arry, smoothx=True, mvx=30)
        pantie = np.uint8(pantie * 255)[60:430, 16:-80]
        pantie = np.bitwise_and(pantie, self.mask)

        # mirroring and finalize
        [r, c, d] = pantie.shape
        npantie = np.zeros((r, c * 2, d), dtype=np.uint8)
        npantie[:, c:, ] = pantie
        npantie[:, :c, ] = pantie[:, ::-1]
        return Image.fromarray(npantie)


    def gen_bra(self, image):
        def pick_color(arr):
            return np.mean(np.mean(arr, axis=0), axis=0)
        pantie = np.array(image)

        # pickup colors
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = pick_color(front)
        front_shade_color = pick_color(front_shade)
        front_shade_color = rgb2hsv(front_shade_color[None, None])
        front_shade_color[0, 0, 1] *= front_shade_color[0, 0, 2] / 0.3
        if front_shade_color[0, 0, 1] > 0.7:
            front_shade_color[0, 0, 1] *= 0.7
        front_shade_color[0, 0, 2] *= front_shade_color[0, 0, 2] / 0.4
        front_shade_color = np.clip(hsv2rgb(front_shade_color)[0, 0], 0, 1)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = pick_color(ribbon_shade)

        # making a center texture
        center = np.rot90(pantie[20:170, -200:-15, :3][::-1], 3)
        center = resize(center, [1.25, 1.25])

        # painting colors
        bra_center = np.copy(self.bra_center)
        bra_center[200:200 + center.shape[0], 315:315 + center.shape[1], :3] = center * np.float32(bra_center[200:200 + center.shape[0], 315:315 + center.shape[1], :3] > 0)
        bra_center[200:200 + center.shape[0], 560:560 + center.shape[1], :3] = center[:, ::-1] * np.float32(bra_center[200:200 + center.shape[0], 560:560 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_frill = self.bra_frill[:, :, :3] * ribbon_color
        bra_ribbon = self.bra_ribbon[:, :, :3] * ribbon_color
        bra_ribbon_shade = (self.bra_ribbon_shade[:, :, -1])[:, :, None] * ribbon_shade_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_frill, bra, self.bra_frill_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = alpha_brend(bra_ribbon, bra, self.bra_ribbon_mask)
        bra = alpha_brend(bra_ribbon_shade, bra, bra_ribbon_shade[:, :, -1])
        bra = np.dstack((bra, self.bra_alpha))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

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
