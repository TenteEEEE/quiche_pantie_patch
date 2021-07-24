from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_sephira.png', **options):
        super().__init__('セフィラ', body=body, pantie_position=[737, 2421], **options)
        self.mask = io.imread('./mask/mask_sephira.png')
        try:
            self.use_ribbon_mesh = self.options['use_ribbon_mesh']
        except:
            self.use_ribbon_mesh = self.ask(question='Use ribbon mesh?', default=True)

        self.bra_position = [136, 1583]
        self.bra = np.float32(io.imread('./mask/bra_sephira.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_sephira_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_sephira_shade.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]

        self.pantie_extra_position = [1624, 3255]
        self.pantie_extra_shade = np.float32(io.imread('./material/sephira_pantie_ext.png') / 255)

        self.bra_extra_position1 = [10, 1786]
        self.bra_extra_position2 = [10, 2958]
        self.bra_extra_shade1 = np.float32(io.imread('./material/sephira_bra_ext1.png') / 255)
        self.bra_extra_shade2 = np.float32(io.imread('./material/sephira_bra_ext2.png') / 255)

        if self.use_ribbon_mesh:
            self.ribbon_position = [1585, 2602]
            self.ribbon_shade = np.float32(io.imread('./material/sephira_ribbon_shade.png') / 255)[:, :, -1]
            self.ribbon = np.float32(io.imread('./material/sephira_ribbon.png') / 255)

    def convert(self, image):
        pantie = np.array(image)
        if self.use_ribbon_mesh:
            pantie = ribbon_inpaint(pantie)

        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = patch[::-1, ::-1]
        front = pantie[:300, :350]
        back = pantie[:-8, 300:][:, ::-1]
        back = np.pad(back, [(0, 100), (0, 0), (0, 0)], 'constant')

        arry = np.zeros(49)
        arry[2:25] = np.sin(np.linspace(0, np.pi, 23)) * -10
        arrx = (np.sin(np.linspace(-np.pi / 2, np.pi, 49)) + 1) * 11.5 - 35
        arrx[:25] -= np.sin(np.linspace(0, np.pi / 2, 25)) * 4
        arrx[-14:] += np.linspace(0, 1, 14)**2 * 20
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(resize(front, [1.87, 1.87]) * 255)[:, 16:]
        front = np.concatenate((front[:, ::-1], front), axis=1)

        arry = np.linspace(0, 1, 49) * -10
        arry[7:21] -= np.sin(np.linspace(0, np.pi / 2, 14)) * 20
        arrx = np.linspace(0, 1, 49)**1.5 * 155 - 155
        arrx[7:-7] -= np.sin(np.linspace(-np.pi, np.pi, 35)) * 6.5
        arrx[:21] -= np.sin(np.linspace(0, np.pi / 2, 21)) * 5
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(resize(back, [1.87, 1.87]) * 255)[:-50, 18:]
        back = np.concatenate((back[:, ::-1], back), axis=1)
        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shiftx = 45
        shifty = 293
        pantie = np.zeros((fr + br - shifty + 25, fc, d), dtype=np.uint8)
        pantie[:fr, :fc] = front
        pantie[shifty:shifty + br, shiftx:shiftx + bc] = alpha_brend(back, pantie[shifty:shifty + br, shiftx:shiftx + bc], back[:, :, -1] > 0.5)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def extract_bra_color(self, pantie):
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        return front_color, front_shade_color

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [4.3, 4.3])
        bra_center = np.copy(self.bra_center)
        bra_center[1715:1715 + center.shape[0], 100:100 + center.shape[1], :3] = center * np.float32(bra_center[1715:1715 + center.shape[0], 100:100 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = np.float32(self.bra_shade[:, :, -1] > 0)[:, :, None] * front_shade_color
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_extra_using_shademap(self, image, shade):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_bra_color(pantie)
        dst = np.zeros_like(shade) + 1.
        dst = dst[:, :, :3] * front_color
        dst_shade = np.float32(shade[:, :, -1] > 0)[:, :, None] * front_shade_color
        dst = alpha_brend(dst_shade, dst, shade[:, :, -1])
        dst = np.dstack((dst, dst[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(dst, 0, 1) * 255))

    def gen_ribbon(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)
        ribbon = self.ribbon[:, :, :3] * ribbon_color
        ribbon_shade = np.float32(self.ribbon_shade > 0)[:, :, None] * ribbon_shade_color
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
        patched = self.paste(patched, self.gen_extra_using_shademap(image, self.pantie_extra_shade), self.pantie_extra_position)
        patched = self.paste(patched, self.gen_extra_using_shademap(image, self.bra_extra_shade1), self.bra_extra_position1)
        patched = self.paste(patched, self.gen_extra_using_shademap(image, self.bra_extra_shade2), self.bra_extra_position2)
        if self.use_ribbon_mesh:
            patched = self.paste(patched, self.gen_ribbon(image), self.ribbon_position)
        return patched
