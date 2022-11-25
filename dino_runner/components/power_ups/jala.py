from dino_runner.utils.constants import JALA, JALA_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Jala(PowerUp):
    def __init__(self):
        self.image = JALA
        self.type = JALA_TYPE        
        super().__init__(self.image, self.type)
