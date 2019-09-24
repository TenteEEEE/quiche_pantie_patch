import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.filters import gaussian


class patcher(patcher):
    def __init__(self, body='./body/body_yuko.png', **options):
        super().__init__('幽狐', body=body, pantie_position=[1, 1130], **options)
        self.mask = io.imread('./mask/mask_yuko.png')
        self.ribbon_position = [1712, 1601]
        self.bra_position = [298, 1301]
        try:
            self.use_ribbon_mesh = self.options['use_ribbon_mesh']
        except:
            self.use_ribbon_mesh = self.ask(question='Use Yuko ribbon mesh?', default=False)
        if self.use_ribbon_mesh:
            self.ribbon_base = io.imread('./mask/ribbon_yuko.png')[:, :, :3] / 255
            self.ribbon_shade = io.imread('./material/ribbon_yuko.png')[:, :, 3] / 255

        self.bra_base = io.imread('./mask/bra_yuko.png')[1300:, 300:-400] / 255
        self.bra_mask = self.bra_base[:, :, 0] > 0
        self.bra_center = io.imread('./mask/bra_yuko_center.png')[1300:, 300:-400, 0] > 0
        self.bra_shade = io.imread('./material/bra_yuko_shade.png')[1300:, 300:-400, 3] / 255
        self.frill = io.imread('./material/bra_yuko_frill.png')[1300:, 300:-400] / 255
        self.lace = io.imread('./material/bra_yuko_lace.png')[1300:, 300:-400] / 255
        self.ribbon_mask = io.imread('./mask/ribbon.png')

    def gen_ribbon(self, image):
        image = np.array(image)
        ribbon = image[19:58, 5:35, :3]
        base_color = np.mean(np.mean(ribbon[5:12, 16:20], axis=0), axis=0) / 255
        shade_color = np.mean(np.mean(ribbon[8:14, 7:15], axis=0), axis=0) / 255
        ribbon_base = io.imread('./mask/ribbon_yuko.png')[:, :, :3] / 255
        ribbon_shade = io.imread('./material/ribbon_yuko.png')[:, :, 3] / 255
        ribbon_base = (self.ribbon_base > 0) * base_color
        ribbon_shade = self.ribbon_shade[:, :, None] * (1 - shade_color)
        ribbon = ribbon_base - ribbon_shade
        ribbon = np.dstack((ribbon, ribbon[:, :, 0] > 0))
        ribbon = np.clip(ribbon, 0, 1)
        return Image.fromarray(np.uint8(ribbon * 255))

    def gen_bra(self, image):
        # image = Image.open('./dream/0101.png')
        pantie = np.array(image)
        if self.use_ribbon_mesh:
            pantie = ribbon_inpaint(pantie)
        else:
            ribbon = pantie.copy()
            ribbon[:, :, 3] = self.ribbon_mask[:, :, 1]
            ribbon = ribbon[19:58, 8:30] / 255.0

        front = pantie[20:100, 30:80, :3] / 255
        front_shade = pantie[100:150, 0:40, :3] / 255
        center = pantie[20:170, -200:-15, :3] / 255
        base_color = np.mean(np.mean(center, axis=0), axis=0)
        front_color = np.mean(np.mean(front, axis=0), axis=0)
        shade_color = np.mean(np.mean(front_shade, axis=0), axis=0)

        # make seamless design
        design = rgb2gray(center[:, :, :3])[::-1, ::-1]
        design = (design - np.min(design)) / (np.max(design) - np.min(design))
        edge = 3
        design_seamless = gaussian(design, sigma=3)
        design_seamless[edge:-edge, edge:-edge] = design[edge:-edge, edge:-edge]
        [hr, hc, hd] = center.shape
        y = np.arange(-hr / 2, hr / 2, dtype=np.int16)
        x = np.arange(-hc / 2, hc / 2, dtype=np.int16)
        design_seamless = (design_seamless[y, :])[:, x]  # rearrange pixels
        design_seamless = resize(design_seamless, [1.65, 1.8])
        design_seamless = np.tile(design_seamless, (3, 4))
        posy = int((self.bra_center.shape[0] - design_seamless.shape[0]) / 2)
        posx = int((self.bra_center.shape[1] - design_seamless.shape[1]) / 2)
        sx = 0
        sy = 0
        design_seamless = (np.pad(design_seamless, [(posy + sy + 1, posy - sy), (posx + sx, posx - sx)], mode='constant'))

        # Base shading
        bra_base = self.bra_base[:, :, :3] * front_color
        bra_base = bra_base - design_seamless[:, :, None] / 10

        shade = rgb2hsv(np.tile((self.bra_shade)[:, :, None], [1, 1, 3]) * base_color)
        shade[:, :, 0] -= 1
        shade[:, :, 1] *= 0.5 + np.mean(base_color) / 3
        shade[:, :, 2] /= 1 + 1 * np.mean(base_color)
        bra_shade = hsv2rgb(shade)

        # bra_shade = bra_shade[:, :, None] * shade_color

        # Center painting
        sx = -270
        sy = -50
        center = resize(center, [4, 4])
        posy = int((self.bra_center.shape[0] - center.shape[0]) / 2)
        posx = int((self.bra_center.shape[1] - center.shape[1]) / 2)
        center = (np.pad(center, [(posy + sy, posy - sy), (posx + sx, posx - sx), (0, 0)], mode='constant'))
        center = center * self.bra_center[:, :, None]

        # Decoration painting
        deco_shade = np.median(pantie[5, :, :3], axis=0) / 255
        frill = np.dstack((self.frill[:, :, :3] * deco_shade, self.frill[:, :, 3]))
        lace = np.dstack((self.lace[:, :, :3] * shade_color, self.lace[:, :, 3]))

        # Finalize
        textured = bra_base * (1 - self.bra_center[:, :, None]) + center * self.bra_center[:, :, None]
        textured = textured - bra_shade
        textured = textured * (1 - lace[:, :, 3])[:, :, None] + lace[:, :, :3] * lace[:, :, 3][:, :, None]
        textured = textured * (1 - frill[:, :, 3])[:, :, None] + frill[:, :, :3] * frill[:, :, 3][:, :, None]
        textured = np.dstack((textured, self.bra_mask))
        if self.use_ribbon_mesh is False:
            ribbon = skt.rotate(ribbon, 8, resize=True)
            ribbon = resize(ribbon, [1.5, 1.5])
            [r, c, d] = ribbon.shape
            textured[460:460 + r, 35:35 + c] = textured[460:460 + r, 35:35 + c] * (1 - ribbon[:, :, 3][:, :, None]) + ribbon * ribbon[:, :, 3][:, :, None]
        return Image.fromarray(np.uint8(np.clip(textured, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)
        [r, c, d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (270, 60), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = np.uint8(patch * 255)

        # Inpainting ribbon
        if self.use_ribbon_mesh:
            pantie = ribbon_inpaint(pantie)

        # Front transform
        front = pantie[:390, :250, :]
        front = np.pad(front, [(0, 0), (50, 0), (0, 0)], mode='constant')
        front = front.transpose(1, 0, 2)
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[40:] -= (np.linspace(0, 1 * np.pi, 60)**2) * 4
        arrx[28:70] += (np.sin(np.linspace(0, 1 * np.pi, 100)) * 10)[28:70]
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(front.transpose(1, 0, 2) * 255)[:, 38:]

        # Back transform
        back = pantie[:350, 250:, :]
        back = np.pad(back, [(0, 0), (0, 100), (0, 0)], mode='constant')
        back = back.transpose(1, 0, 2)
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[10:] -= (np.linspace(0, 1 * np.pi, 90)**3) * 14
        back = affine_transform_by_arr(back, arrx, arry, smoothx=True)
        back = np.uint8(back.transpose(1, 0, 2) * 255.0)[:, 1:]

        # Merge front and back
        pantie = np.zeros((np.max((front.shape[0], back.shape[0])), front.shape[1] + back.shape[1], d), dtype=np.uint8)
        pantie[:front.shape[0], :front.shape[1]] = front
        pantie[:back.shape[0], front.shape[1]:] = back

        # main transform
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[35:] += (np.cos(np.linspace(0, 1 * np.pi, 100) - np.pi) * -75)[35:] - 30
        arrx[:30] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi / 0.9) * 10)[:30]
        arrx[50:80] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi) * 11)[:30]
        arry += np.linspace(0, 1, 100) * -50
        arry[:30] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi) * 35)[:30]
        pantie = affine_transform_by_arr(pantie, arrx, arry, smoothx=True)
        pantie = skt.rotate(pantie, 8.1, resize=True)

        # Finalize
        pantie = resize(pantie, [2.31, 2.31])
        pantie = pantie[140:-80, 72:]
        pantie = np.uint8(pantie * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.use_ribbon_mesh:
            ribbon = self.gen_ribbon(image)
            self.paste(patched, ribbon, self.ribbon_position)
        bra = self.gen_bra(image)
        patched = self.paste(patched, bra, self.bra_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
