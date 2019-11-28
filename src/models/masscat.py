import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_masscat.png', **options):
        super().__init__('量産型のらきゃっと', body=body, pantie_position=[2588, 1047], **options)
        self.mask = io.imread('./mask/mask_masscat.png')
        try:
            self.with_skin = self.options['with_skin']
        except:
            self.with_skin = self.ask(question='Overlay with skin?', default=True)
        if self.with_skin:
            self.skin = Image.open('./material/skin_masscat.png')
            try:
                self.with_socks = self.options['with_socks']
            except:
                self.with_socks = self.ask(question='Wear socks?', default=True)
            if self.with_socks:
                try:
                    self.is_knee = self.options['is_knee']
                except:
                    self.is_knee = self.ask(question='Knee socks?', default=True)
                if self.is_knee:
                    self.socks = Image.open('./material/kneesocks_masscat.png')
                else:
                    self.socks = Image.open('./material/socks_masscat.png')
                    
    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-180:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (200, 65), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        # Front affine transform
        front = pantie[:, :300]
        front[50:, 180:] = 0
        front = skt.rotate(front, -30.9, resize=True)[:, ::-1]
        arrx = (np.linspace(1, 0, 100)**3) * 123 - 20
        arry = np.zeros(100)
        front = affine_transform_by_arr(front, arrx, arry)
        front = (front[:350, :-110] * 255).astype(np.uint8)

        # Back affine transform
        back = pantie[:, 300:]
        back = skt.rotate(back, -150.8, resize=True)
        arrx = np.zeros(100)
        arrx[:50] = (np.linspace(1, 0, 50)**2) * -400
        arrx[40:90] += np.sin(np.linspace(0, np.pi, 50)) * 20
        arry = np.zeros(100)
        arrx += 40
        back = affine_transform_by_arr(back, arrx, arry)
        back = (back[250:-30] * 255).astype(np.uint8)

        def alpha_brend(img1, img2, mask):
            return img1 * mask[:, :, None] + img2 * (1 - mask)[:, :, None]
        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shift_x = 160
        shift_y = 78
        pantie = np.zeros((np.max([fr, br + shift_y]), fc + bc - shift_x, d), dtype=np.uint8)
        pantie[shift_y:shift_y + br, :bc] = alpha_brend(back, pantie[shift_y:shift_y + br, :bc], back[:, :, -1] > 0)
        pantie[:fr, -fc:] = alpha_brend(front, pantie[:fr, -fc:], front[:, :, -1] > 0)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.uint8(resize(pantie, [2.2, 2.2]) * 255)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.with_skin:
            patched = self.paste(patched, self.skin, [0,0])
            if self.with_socks:
                patched = self.paste(patched, self.socks, [0,0])
        patched = self.paste(patched, image, self.pantie_position)
        return patched
