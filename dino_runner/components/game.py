import pygame
import random

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, GAME_OVER, CLOUD
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"
GAME_SPEED = 20
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_STYLE, 22)
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = SCREEN_WIDTH + random.randint(800, 1000) ##
        self.y_pos_cloud = random.randint(30, 150)###
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()        

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()    
        pygame.display.quit()
        pygame.quit()    

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.score =0
        self.game_speed = GAME_SPEED
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def update_score(self): 
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) 
        self.draw_background()
        self.draw_background_cloud()     #############
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):     # TA REPETIDO 
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_background_cloud(self):    
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))          
        self.x_pos_cloud -= self.game_speed
        if self.x_pos_cloud <= -image_width:
            self.x_pos_cloud = SCREEN_WIDTH - random.randint(2500,3000)
            self.y_pos_cloud = random.randint(50, 150)
            self.screen.blit(CLOUD, (image_width +self.x_pos_cloud, self.y_pos_cloud))            
            self.x_pos_cloud  = SCREEN_WIDTH

    def text_draw(self, text, x, y ): 
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text, text_rect)   

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.text_draw(text, 1000, 50)

    def handle_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN: # não confuda: K_DOWN
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        if self.death_count == 0:
            text = self.font.render("Press any key to start", True, (0, 0, 0))
            self.text_draw(text, HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT )
        else:        
            self.screen.blit(ICON, (HALF_SCREEN_WIDTH - 20, HALF_SCREEN_HEIGHT - 140)) 
            self.screen.blit(GAME_OVER, (HALF_SCREEN_WIDTH -180, HALF_SCREEN_HEIGHT + 100)) 
            text = self.font.render("Press any Key to Restart", True, (0,0,0))
            self.text_draw(text, HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)
            text = self.font.render(f"Your Score: {str(self.score)} and Count of Death {str(self.death_count)}", True,(0,0,0))
            self.text_draw(text, HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT-200 )

        pygame.display.update()
        self.handle_events_menu()
    