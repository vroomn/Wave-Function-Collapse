import pygame
from enum import Enum
import random
from collections import namedtuple

BOXSCALAR = 99 # How big the boxes are gonna be (both width and height)

pygame.init()
screen = pygame.display.set_mode((BOXSCALAR*5, BOXSCALAR*5)) # 5x5 99 pixel area
clock = pygame.time.Clock()


tileShape = namedtuple("tileShape", ["top", "right", "bottom", "left", "center"]) # Allows for syntax assistance while programming
class Tile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
        self.rect = pygame.Rect(self.x, self.y, BOXSCALAR, BOXSCALAR)
        self.surface = pygame.Surface((BOXSCALAR, BOXSCALAR))
        #self.surface.fill(pygame.Color(int((x/BOXSCALAR)*51), int((y/BOXSCALAR)*51), 255)) Fun color
        self.surface.fill(pygame.Color(99, 173, 149)) # Non collapsed color

        self.shape: tileShape = None

    def collapse(self):
        pass

    def __str__(self) -> str: # Identifies the tile when printed
        return f"""Tile of shape: {self.shape} at position: ({self.x}, {self.y})"""

    def draw(self) -> None:
        screen.blit(self.surface, self.rect)

tiles = []
for row in range(0, 5):
    print()
    for column in range(0, 5):
        addition = Tile(row*BOXSCALAR, column*BOXSCALAR)
        tiles.append(addition)
        print(addition)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit when the close button is pressed

    # ACTUAL RENDERING ------------------------------------------------------
    pygame.display.flip() # Swaps the buffers
    screen.fill(pygame.Color(122, 122, 122))

    for tile in tiles:
        tile.draw()

    # -----------------------------------------------------------------------

    clock.tick(60) # Lock off to 60 FPS

pygame.quit()