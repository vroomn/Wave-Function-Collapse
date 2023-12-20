import pygame

pygame.init()
screen = pygame.display.set_mode((320, 320)) # 5x5 64 pixel area
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit when the close button is pressed

    # ACTUAL RENDERING ------------------------------------------------------
    pygame.display.flip() # Swaps the buffers
    screen.fill(pygame.Color(122, 122, 122))
    # -----------------------------------------------------------------------

    clock.tick(60) # Lock off to 60 FPS

pygame.quit()