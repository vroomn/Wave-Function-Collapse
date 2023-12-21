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
        self.isCollapsed = True
        collapsedSectors = [
            False, # Top
            False, # Right
            False, # Bottom
            False, # Left
            False] # Center

        def localCollapse(xDir, yDir, tmp: int):
            idx = (int((self.x+BOXSCALAR*xDir)/BOXSCALAR)*BOXES) + int((self.y+(BOXSCALAR*yDir))/BOXSCALAR)
            if idx >= 0 and idx < len(tiles) and tiles[idx].isCollapsed == True:
                tileAbove: Tile = tiles[idx]
                if tmp == 0:
                    if tileAbove.shape.bottom:
                        collapsedSectors[tmp] = True
                    else:
                        collapsedSectors[tmp] = False
                elif tmp == 1:
                    if tileAbove.shape.left:
                        collapsedSectors[tmp] = True
                    else:
                        collapsedSectors[tmp] = False
                elif tmp == 2:
                    if tileAbove.shape.top:
                        collapsedSectors[tmp] = True
                    else:
                        collapsedSectors[tmp] = False
                elif tmp == 3:
                    if tileAbove.shape.right:
                        collapsedSectors[tmp] = True
                    else:
                        collapsedSectors[tmp] = False
            else:
                collapsedSectors[tmp] = bool(random.randrange(0, 2)) # Because the tile above is out of range, this tile sector decides how to collapse
        
        localCollapse(0, -1, 0)
        localCollapse(1, 0, 1)
        localCollapse(0, 1, 2)
        localCollapse(-1, 0, 3)
        
        for i in collapsedSectors:
            if i == True:
                collapsedSectors[4] = True
                break

        self.shape: tileShape = tileShape(collapsedSectors[0], collapsedSectors[1], collapsedSectors[2], collapsedSectors[3], collapsedSectors[4])
        #print(self)

        colorStep = 255/BOXES
        self.surface.fill(pygame.Color(int((self.x/BOXSCALAR)*colorStep), int((self.y/BOXSCALAR)*colorStep), 255)); "Fun color"

    def __str__(self) -> str: # Identifies the tile when printed
        return f"""Tile of shape: {self.shape} at position: ({self.x}, {self.y})"""

    def draw(self) -> None:
        offset = BOXSCALAR/3
        tmpRect = pygame.Rect(0, 0, offset, offset)
        tmpSurface = pygame.Surface((offset, offset))
        tmpSurface.fill(pygame.Color(117, 12, 50), tmpRect)

        if self.shape.bottom:
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

tiles = []
for row in range(0, BOXES):
    #print()
    for column in range(0, BOXES):
        addition = Tile(row*BOXSCALAR, column*BOXSCALAR)
        tiles.append(addition)

for tile in tiles:
    tile.collapse()

def totalCollapse():
    pass

#totalCollapse()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit when the close button is pressed
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                for tile in tiles:
                    tile.collapse()"""

    # ACTUAL RENDERING ------------------------------------------------------
    pygame.display.flip() # Swaps the buffers
    screen.fill(pygame.Color(122, 122, 122))

    for tile in tiles:
       tile.draw()

    # -----------------------------------------------------------------------

    clock.tick(60) # Lock off to 60 FPS

pygame.quit()
# idx = int(tile.y/BOXSCALAR) + (int(tile.x/BOXSCALAR)*BOXES) # Formula to calulate index in array from position