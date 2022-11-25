import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.jala import Jala
from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE, JALA_TYPE


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
       
    def generate_power_up(self, score):
        power_up_type = [Hammer(), Shield(), Jala()]
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)    ####          
            self.power_ups.append(power_up_type[random.randint(0,2)])  
             
    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.has_power_up = True
                player.type = power_up.type                
                if power_up.type == SHIELD_TYPE:  
                    player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                    self.power_ups.remove(power_up)      
                    player.shield = True             
                elif power_up.type == HAMMER_TYPE:
                    player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                    self.power_ups.remove(power_up)
                    player.hammer = True
                elif power_up.type == JALA_TYPE:
                    player.power_up_time = power_up.start_time + (power_up.duration * 2000)
                    self.power_ups.remove(power_up)
                    player.jala = True

                
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
            
    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)