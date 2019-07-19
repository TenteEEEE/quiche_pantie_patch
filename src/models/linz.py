from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_linz.png', **options):
        super().__init__('Linz', body=body, pantie_position=[1017, 828], **options)
