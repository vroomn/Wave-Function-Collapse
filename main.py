import pygame
from enum import Enum
import random
from collections import namedtuple

BOXSCALAR = 99 # How big the boxes are gonna be (both width and height)
BOXES = 5 # How many boxes are on each side

pygame.init()
screen = pygame.display.set_mode((BOXSCALAR*BOXES, BOXSCALAR*BOXES)) # 5x5 99 pixel area
clock = pygame.time.Clock()

tileShape = namedtuple("tileShape", ["top", "right", "bottom", "left", "center"]) # Allows for syntax assistance while programming
class Tile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.isCollapsed = False
        
        self.rect = pygame.Rect(self.x, self.y, BOXSCALAR, BOXSCALAR)
        self.surface = pygame.Surface((BOXSCALAR, BOXSCALAR))
        #colorStep = 255/BOXES
        #self.surface.fill(pygame.Color(int((x/BOXSCALAR)*colorStep), int((y/BOXSCALAR)*colorStep), 255)); "Fun color"
        self.surface.fill(pygame.Color(99, 173, 149)) # Non collapsed color

        self.shape: namedtuple = tileShape(False, False, False, False, False)
        self.entropy: int = 5

    def collapse(self):
        def localCollapse(xChange, yChange) -> bool:
            collapse: bool = None
            # Look north and see what there is
            idx = int((self.y+yChange)/BOXSCALAR) + (int((self.x+xChange)/BOXSCALAR)*BOXES) # Formula to calulate index in array from position
            print(f"IDX: {idx}")
            if idx >= 0:
                tile: Tile = tiles[idx]
                if tile.isCollapsed == True:
                    if tile.shape.bottom == True:
                        collapse = bool(random.getrandbits(1))
                        if collapse:
                            tiles[idx].entropy -= 1
                        return collapse
                else:
                    collapse = bool(random.getrandbits(1))
                    if collapse:
                        tiles[idx].entropy -= 1
                    return collapse
            
            # If all else fails
            return False

        collapsedSectors = [
            localCollapse(0, -BOXSCALAR),
            localCollapse(+BOXSCALAR, 0),
            localCollapse(0, +BOXSCALAR),
            localCollapse(-BOXSCALAR, 0),
            False]
        
        for i in collapsedSectors:
            if i == True:
                collapsedSectors[4] = True
                break

        self.shape: tileShape = tileShape(collapsedSectors[0], collapsedSectors[1], collapsedSectors[2], collapsedSectors[3], collapsedSectors[4])
        print(self)

        colorStep = 255/BOXES
        self.surface.fill(pygame.Color(int((self.x/BOXSCALAR)*colorStep), int((self.y/BOXSCALAR)*colorStep), 255)); "Fun color"

    def __str__(self) -> str: # Identifies the tile when printed
        return f"""Tile of shape: {self.shape} at position: ({self.x}, {self.y})"""

    def draw(self) -> None:
        offset = BOXSCALAR/3
        tmpRect = pygame.Rect(0, 0, offset, offset)
        tmpSurface = pygame.Surface((offset, offset))
        tmpSurface.fill(pygame.Color(117, 12, 50), tmpRect)
        if self.shape.bottom == True:
            self.surface.blit(tmpSurface, tmpRect.move(offset, offset*2))

        if self.shape.top:
            self.surface.blit(tmpSurface, tmpRect.move(offset, 0))

        if self.shape.center:
            self.surface.blit(tmpSurface, tmpRect.move(offset, offset))

        if self.shape.left:
            self.surface.blit(tmpSurface, tmpRect.move(0, offset))

        if self.shape.right:
            self.surface.blit(tmpSurface, tmpRect.move(offset*2, offset))

        screen.blit(self.surface, self.rect)

unCollapsedTiles = []
tiles = []
for row in range(0, BOXES):
    #print()
    for column in range(0, BOXES):
        addition = Tile(row*BOXSCALAR, column*BOXSCALAR)
        tiles.append(addition)

tiles[3].collapse()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit when the close button is pressed

    # ACTUAL RENDERING ------------------------------------------------------
    pygame.display.flip() # Swaps the buffers
    screen.fill(pygame.Color(122, 122, 122))

    #for tile in tiles:
    #    tile.draw()
    tiles[3].draw()
    tiles[2].draw()
    tiles[8].draw()
    tiles[4].draw()

    # -----------------------------------------------------------------------

    clock.tick(60) # Lock off to 60 FPS

pygame.quit()
# idx = int(tile.y/BOXSCALAR) + (int(tile.x/BOXSCALAR)*BOXES) # Formula to calulate index in array from position