import pygame
import sys
from time import sleep
from gol import initialize_grid, update_grid

pygame.init()

X_RESOLUTION = 800
Y_RESOLUTION = 600
X_CELLS = 20
Y_CELLS = 20
CELL_WIDTH = X_RESOLUTION // X_CELLS
CELL_HEIGHT = Y_RESOLUTION // Y_CELLS

grid = [[0 for _ in range(X_CELLS)] for _ in range(Y_CELLS)]

grid[0][1] = 1
grid[1][2] = 1
grid[2][0] = 1
grid[2][1] = 1
grid[2][2] = 1

# Set up the display
screen = pygame.display.set_mode((X_RESOLUTION, Y_RESOLUTION))
pygame.display.set_caption('Gol')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a background color
    screen.fill((0, 0, 0))
    # Draw the cells
    for x in range(X_CELLS):
        for y in range(Y_CELLS):
            rect = pygame.Rect(x*CELL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            if grid[y][x] == 1:  # Fill cell if active
                pygame.draw.rect(screen, (255, 255, 255), rect)

    grid = update_grid(grid, X_CELLS, Y_CELLS)
    sleep(0.1)
    # Draw the grid lines after filling cells to ensure they remain visible
    for x in range(X_CELLS + 1):
        pygame.draw.line(screen, (255, 255, 255), (x*CELL_WIDTH, 0), (x*CELL_WIDTH, Y_RESOLUTION))
    for y in range(Y_CELLS + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, y*CELL_HEIGHT), (X_RESOLUTION, y*CELL_HEIGHT))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
