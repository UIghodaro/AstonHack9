import json
import pygame

NEIGHBOUR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=48):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        
        #A for loop that fills the tilemap dictionary with tiles and information about them
        #Namely information on the type, their (picture) variant and position
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}
    
    #This function feels like magic, would never think of it myself it's insane optimisation
    #Checks what tiles are nearby the player, by retrieving the players position and then manually selecting all tiles next to it
    #Then appends the ID of these tiles into a list and returns it - for collision detection
    def nearby_tiles(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))  #Cast to int because pos[0] may truncate a float to an integer, but it'd still have a float datatype
        for offset in NEIGHBOUR_OFFSETS:
            check = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check in self.tilemap:
                tiles.append(self.tilemap[check])
        
        return tiles
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def physics_rect_around(self, pos):
        rects = []
        for tile in self.nearby_tiles(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))     #Recall, rect takes in: (x position, y position, width, height)
            
        return rects
            
    #This function is a fucking lot
    #This is a for-each loop, 'loc' essentially being i, it blits each tile (defined in the assets dictionary in game.py) onto the screen based on the tile position (accounting for its size), referred to above  
    #Where surf = surface
    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
               
        #Below is a for loop, detecting the location of the screen/camera currently (with error) and making it such that only tiles in view of the screen are rendered
        #Essentially works by iterating through the screen itself, bit by bit, top right to bottom left
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
    
        #This code used to just blit everything onto the screen, regardless of if the camera could see it or not
        #for loc in self.tilemap:
        #    tile = self.tilemap[loc]
        #    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))