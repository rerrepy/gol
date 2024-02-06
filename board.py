import pygame
import sys
from time import sleep
from gol import initialize_grid, update_grid, initialize_alive_cells

pygame.init()

# Screen setup
GRID_WIDTH = 1600
GRID_HEIGHT = 1200
CONTROL_WIDTH = 200  # Width of the control panel
TOTAL_WIDTH = GRID_WIDTH + CONTROL_WIDTH  # Total screen width
Y_RESOLUTION = GRID_HEIGHT
X_CELLS = 400
Y_CELLS = 300
CELL_WIDTH = GRID_WIDTH // X_CELLS
CELL_HEIGHT = Y_RESOLUTION // Y_CELLS

grid = initialize_grid(X_CELLS, Y_CELLS)

#grid = [[0 for _ in range(X_CELLS)] for _ in range(Y_CELLS)]

grid[0][1] = 1
grid[1][2] = 1
grid[2][0] = 1
grid[2][1] = 1
grid[2][2] = 1
alive_cells = initialize_alive_cells(grid)


def place_glider_gun(grid, top_left_x, top_left_y):
    # Clear the area where the glider gun will be placed
    for i in range(top_left_y, top_left_y + 11):
        for j in range(top_left_x, top_left_x + 38):
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                grid[i][j] = 0
                
    # Place the glider gun pattern onto the grid
    offsets = [
        (4, 0), (4, 1), (5, 0), (5, 1),
        (4, 10), (5, 10), (6, 10), (3, 11), (7, 11),
        (2, 12), (8, 12), (2, 13), (8, 13), (5, 14),
        (3, 15), (7, 15), (4, 16), (5, 16), (6, 16),
        (5, 17), (2, 20), (3, 20), (4, 20), (2, 21),
        (3, 21), (4, 21), (1, 22), (5, 22), (0, 24),
        (1, 24), (5, 24), (6, 24), (2, 34), (3, 34),
        (2, 35), (3, 35)
    ]
    
    for y_offset, x_offset in offsets:
        y = top_left_y + y_offset
        x = top_left_x + x_offset
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            grid[y][x] = 1

# The rest of your code goes here
glider_gun_pattern = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def draw_pattern_preview(screen, pattern, top_left_x, top_left_y, cell_width, cell_height, preview_color):
    # Draw an overlay of the pattern at the given top-left corner with a distinct color.
    for y, row in enumerate(pattern):
        for x, cell in enumerate(row):
            if cell:
                # Use top_left_x and top_left_y directly as they are already grid coordinates
                rect = pygame.Rect(top_left_x + x * cell_width, top_left_y + y * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, preview_color, rect)


def place_pattern(grid, pattern, top_left_x, top_left_y):
    # This function will place the pattern onto the grid at the given top-left corner.
    for y, row in enumerate(pattern):
        for x, cell in enumerate(row):
            if 0 <= top_left_y + y < len(grid) and 0 <= top_left_x + x < len(grid[0]):
                grid[top_left_y + y][top_left_x + x] = cell  # Set the cell state



# Display setup
screen = pygame.display.set_mode((TOTAL_WIDTH, Y_RESOLUTION))
pygame.display.set_caption('Gol')

# Button setup
font = pygame.font.Font(None, 36)
pause_button = pygame.Rect(GRID_WIDTH + 30, 10, 160, 50)
speed_button = pygame.Rect(GRID_WIDTH + 30, 70, 160, 50)
slow_button = pygame.Rect(GRID_WIDTH + 30, 130, 160, 50)
# Add a button for the "glider gun"
glider_gun_button = pygame.Rect(GRID_WIDTH + 30, 190, 160, 50)

clear_button = pygame.Rect(GRID_WIDTH + 30, 250, 160, 50)

# Add a flag to determine if we are in "glider gun" placement mode
placing_glider_gun = False

# Game state
running = True
paused = False
speed = 0.1  # Speed of simulation

# Initialize Clock for FPS tracking
clock = pygame.time.Clock()

# Initialize font for FPS counter
fps_font = pygame.font.Font(None, 24)  # Smaller font for FPS

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if pause button is clicked
            if pause_button.collidepoint(mouse_x, mouse_y):
                paused = not paused
            # Check if speed button is clicked
            elif speed_button.collidepoint(mouse_x, mouse_y):
                speed = max(0.01, speed - 0.05)  # Decrease delay to speed up
            # Toggle cell state on click
            elif slow_button.collidepoint(mouse_x, mouse_y):
                speed = max(0.01, speed + 0.05)
                       # Check for glider gun button click
            elif glider_gun_button.collidepoint(mouse_x, mouse_y):
                placing_glider_gun = not placing_glider_gun  # Toggle placement mode
            
            # Check for grid click to place the glider gun
            elif placing_glider_gun and mouse_x < GRID_WIDTH:
                cell_x = mouse_x // CELL_WIDTH
                cell_y = mouse_y // CELL_HEIGHT
                place_glider_gun(grid, cell_x, cell_y)
                alive_cells = initialize_alive_cells(grid)
                placing_glider_gun = False  # Exit placement mode after placing
            elif clear_button.collidepoint(mouse_x, mouse_y):
                grid = initialize_grid(X_CELLS, Y_CELLS)
                alive_cells = initialize_alive_cells(grid)
            else:
                cell_x = mouse_x // CELL_WIDTH
                cell_y = mouse_y // CELL_HEIGHT
                if 0 <= cell_x < X_CELLS and 0 <= cell_y < Y_CELLS:
                    grid[cell_y][cell_x] = 1 - grid[cell_y][cell_x]  # Toggle state
                    alive_cells = initialize_alive_cells(grid)

    # Fill the screen with a background color
    screen.fill((255, 255, 255))
    # Draw the cells
    # Use alive_cells directly:
    for cell in alive_cells:
        x, y = cell
        rect = pygame.Rect(x*CELL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 0), rect)

    # Draw the grid lines after filling cells to ensure they remain visible
    for x in range(X_CELLS + 1):
        pygame.draw.line(screen, (0, 0, 0), (x*CELL_WIDTH, 0), (x*CELL_WIDTH, Y_RESOLUTION))
    for y in range(Y_CELLS + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, y*CELL_HEIGHT), (GRID_WIDTH, y*CELL_HEIGHT))

    # Draw pause and speed buttons in the control panel area
    pygame.draw.rect(screen, (100, 100, 100), pause_button)
    pause_text = font.render('Pause' if not paused else 'Resume', True, (255, 255, 255))
    screen.blit(pause_text, (pause_button.x + 20, pause_button.y + 10))

    pygame.draw.rect(screen, (100, 100, 100), speed_button)
    speed_text = font.render('Speed Up', True, (255, 255, 255))
    screen.blit(speed_text, (speed_button.x + 10, speed_button.y + 10))
    
    pygame.draw.rect(screen, (100, 100, 100), slow_button)
    slow_text = font.render('Speed down', True, (255, 255, 255))
    screen.blit(slow_text, (slow_button.x + 10, slow_button.y + 10))

    # Draw the "glider gun" button
    pygame.draw.rect(screen, (100, 100, 100), glider_gun_button)
    glider_gun_text = font.render('Glider Gun', True, (255, 255, 255))
    screen.blit(glider_gun_text, (glider_gun_button.x + 10, glider_gun_button.y + 10))

    pygame.draw.rect(screen, (100, 100, 100), clear_button)
    clear_text = font.render('Clear', True, (255, 255, 255))
    screen.blit(clear_text, (clear_button.x + 10, clear_button.y + 10))


    if placing_glider_gun:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < GRID_WIDTH:
            hover_x = (mouse_x // CELL_WIDTH) * CELL_WIDTH
            hover_y = (mouse_y // CELL_HEIGHT) * CELL_HEIGHT
            draw_pattern_preview(screen, glider_gun_pattern, hover_x, hover_y, CELL_WIDTH, CELL_HEIGHT, (200, 200, 0))
            # Draw a transparent rectangle for preview
            rect = pygame.Rect(hover_x, hover_y, CELL_WIDTH * 38, CELL_HEIGHT * 11)
            #pygame.draw.rect(screen, (255, 255, 0, 128), rect, 1)  # Semi-transparent

    

    if not paused:
        # Update grid if not paused
        grid, alive_cells = update_grid(grid, alive_cells, X_CELLS, Y_CELLS)
        sleep(speed)

    # FPS Counter
    fps = int(clock.get_fps())  # Get the current FPS
    fps_text = fps_font.render(f'FPS: {fps}', True, (0, 0, 0))
    fps_text_rect = fps_text.get_rect(bottomright=(TOTAL_WIDTH - 10, Y_RESOLUTION - 10))
    screen.blit(fps_text, fps_text_rect)
    clock.tick(300)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
