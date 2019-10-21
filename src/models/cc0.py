import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *

class patcher(patcher):
    def __init__(self, body='./body/body_cc0.png', **options):
        super().__init__('cc0', body=body, pantie_position=[407, 838], **options)
        try:
            self.is_4k = self.options['is_4k']
        except:
            self.is_4k = self.ask(question='4K(4096x4096) resolution texture?', default=False)
            
    def convert(self, image):
        pantie = np.array(image)
        arrx = np.zeros(100)
        arry = np.zeros(100)
        arry[5:45] -= np.sin(np.linspace(0, 1 * np.pi, 40)) * 50
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie = pantie[:,11:]
        pantie = np.concatenate((pantie[:,::-1], pantie),axis=1)
        pantie = np.uint8(pantie * 255)
        return Image.fromarray(pantie)
        
    def patch(self, image, transparent=False):
        image = self.convert(image)
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
            image = image.resize((int(image.width * 2), int(image.height * 2)), resample=Image.BICUBIC)
        patched = self.paste(patched, image, pantie_position)
        return patched
