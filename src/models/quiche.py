from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body.png', **options):
        super().__init__(name='キッシュ', body=body, pantie_position=[1018, 828], **options)
