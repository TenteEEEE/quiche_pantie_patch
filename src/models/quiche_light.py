from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_light.png', **options):
        super().__init__('キッシュ(ライト)', body=body, pantie_position=[532, 385], **options)

    def convert(self, image):
        image = image.resize((236, 157))
        return image
