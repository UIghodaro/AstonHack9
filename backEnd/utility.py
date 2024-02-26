import pygame
import os

BASE_IMG_PATH = 'gameRss/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []     #For interaction with the Tilemap class
    
    #pretty much runs through directory, appending EVERY FILE in that directory to the list in the given format
    for img_name in os.listdir(BASE_IMG_PATH + path):   
        images.append(load_image(path+'/'+img_name))
        
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    #An instance of the Animation class is made, using parameters.
    #Whenever this function is called, that same instance will be looked at, hence taking up no more memory
    #It's kinda like when you do "int[] listA = listB;" Where B is an initialised list. A copy of listB isn't made, listA just refers to the same memory location as listB 
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    #This function updates the animation in a loop via the modulus function
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            #If loop turns off (aka the character action changes), the character will flick to a certain frame and then end
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
                
    #Legitimately just returning the images
    def img(self):
        return self.images[int(self.frame / self.img_duration)]