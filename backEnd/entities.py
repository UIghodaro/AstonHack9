import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, 'left': False, 'right' : False}    #To keep track of what collisions are currently happening

        self.action = ''    #What the character is currently doing
        self.anim_offset = (-3, -3)   #This is as sometimes the animation may be larger than the player hitbox
        self.flip = False       #Characters can turn around lmfao
        self.set_action('idle')     #I love homogeneity
        
    #Creating a rect for the entity for the sake of collisions
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    #This is intended for when it comes to changing animations
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement = (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.collisions = {'up' : False, 'down' : False, 'left': False, 'right' : False}    #Updates the collisions detected - if you are no longer at a wall you aren't at a wall n that
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        
        movementModifier = 4
        self.pos[0] += frame_movement[0]*movementModifier
        
        #Collision handling - if you bash into something, you snap the opposite way
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
            
        self.pos[1] += frame_movement[1]
        #As above, but on the y axis
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        #Uses current movement press in place of velocity to determine whether to flip or not, which is intuitive but sucks for me
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)   #The player can fall with a terminal velocity of 5
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        self.animation.update()
    
    #This function renders the entity's animation, since it is here it can also flip the animation before rendering so that things happen as required
    #This might change drastically, due to the nature of the ice
    def render(self, surf, offset):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
    
    def update(self, tilemap, movement = (0,0)):
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        
        if self.collisions['down']:
            self.air_time = 0
            
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')