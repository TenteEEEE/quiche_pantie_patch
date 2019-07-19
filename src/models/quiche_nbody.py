from PIL import Image, ImageOps
from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_quiche_nbody.png', **options):
        super().__init__('Quiche-Nbody', body=body, pantie_position=[403, 836], **options)
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            import src.models.quiche_bra as bra
            self.bra_patcher = bra.patcher(options=options)

    def convert(self, image):
        cut = 7
        right_pantie = image.crop((cut, 0, image.size[0], image.size[1]))
        left_pantie = ImageOps.mirror(right_pantie)
        npantie = Image.new("RGBA", (right_pantie.size[0] * 2, right_pantie.size[1]))
        npantie.paste(right_pantie, (right_pantie.size[0], 0))
        npantie.paste(left_pantie, (0, 0))
        return npantie

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.with_bra:
            bra = self.bra_patcher.convert(image)
            self.paste(patched, bra, self.bra_patcher.pantie_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
