import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE, JALA_TYPE, SOUND
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.sound = SOUND

    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]

        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0,1)])
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):                                                  
                if not game.player.has_power_up:
                    self.sound[0].play()                   
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.type == HAMMER_TYPE:                    
                    self.obstacles.remove(obstacle)
                elif game.player.type == SHIELD_TYPE:
                    game.playing = True
                elif game.player.type == JALA_TYPE:
                    game.game_speed = 100
                    game.playing = True 
                    self.sound[3].play()
                    self.sound[2].stop()                                
                    self.sound[1].stop()
                    self.sound[0].stop()

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):      
        for obstacle in self.obstacles:
            obstacle.draw(screen)
