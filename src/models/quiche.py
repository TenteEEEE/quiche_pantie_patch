from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body.png'):
        super().__init__('Quiche', body=body, pantie_position=[1018, 828])
