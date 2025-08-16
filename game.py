import sys
import pygame
from backEnd.entities import PhysicsEntity, Player
from backEnd.utility import load_image, load_images, Animation
from backEnd.map import Tilemap
from backEnd.clouds import Clouds

class Game:
    
    #This initialises the game, by initialising pygame itself and base assets for the first screen
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("One Skater Smashed")
        self.screen = pygame.display.set_mode((800, 600))   #creates the screen
        self.display = pygame.Surface((400,300))    #We render on a smaller screen and scale it up actually
        
        self.clock = pygame.time.Clock()    #For 60 FPS reasons, see below
        self.movement = [False, False]      #Player can't really start moving innit
        self.assets = {                     #Loading game assets
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=10),
            'player/run': Animation(load_images('entities/player/run'), img_dur=7),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }
        
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.player = Player(self, (50, 50), (46,49))   #See entities.py
        self.tilemap = Tilemap(self, tile_size=48)  #Loading the world map, see map.py
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]    #Starting pos functionality
        
    #This function is for running the game, this is what is updated 60 times per seconds and makes the game "move," per se
    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            #The background - comment this line out if it's hurting your eyes
            self.display.blit(pygame.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))
            
            #????
            #This is magic btw don't ask me what the fuck this is
            #It controls the camera, is all
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)
            
            self.tilemap.render(self.display, offset = render_scroll)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))    #Uses a boolean equation such that if the left and right movements are pressed at the same time, the player stops moving
            self.player.render(self.display, offset = render_scroll)
            
            #Event handling segment
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    
                    
                    #self.player.velocity[0] += (self.movement[1] - self.movement[0]) * min(7, self.player.velocity[0])
                    
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()     #Updates the display so changes actually happen
            self.clock.tick(60)     #60 FPS baby


Game().run()
