from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_light.png'):
        super().__init__('Quiche-Light', body=body, pantie_position=[532, 385])

    def convert(self, image):
        image = image.resize((236, 157))
        return image
