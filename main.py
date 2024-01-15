import pygame
import numpy as np

pygame.init()

# Get actual drawable area for accurate fullscreen calculations
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

# Set cell size based on screen dimensions
cell_size = min(width, height) // 70  # Adjust the divisor as needed for the desired cell size

# Calculate grid dimensions to fill the screen
grid_width = width // cell_size + 1  # + 1 ensure it covers the whole screen width
grid_height = height // cell_size

# Initialize the grid with walls on the border and random values inside
grid = np.zeros((grid_width, grid_height))
grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = 1  # Set border cells to 1

grid[1:-1, 1:-1] = np.random.choice([0, 1], size=(grid_width - 2, grid_height - 2), p=[0.7, 0.3])

# Set colors
pebble_color = (128, 128, 128)
wall_color = (0, 0, 0)
empty_color = (255, 255, 255)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Create a copy of the grid to store the next state
    new_grid = np.copy(grid)

    # Update the grid based on modified rules for cave generation
    for x in range(grid_width):
        for y in range(grid_height):
            # Count live neighbors
            neighbors = np.sum(grid[max(0, x - 1):min(grid_width, x + 2), max(0, y - 1):min(grid_height, y + 2)])

            # Apply modified rules for cave generation
            if neighbors > 4:
                new_grid[x, y] = 1  # Wall
            elif neighbors < 3:
                new_grid[x, y] = 0  # Empty
            elif (
                    grid[x, (y - 1) % grid_height] == 1 and  # Above
                    grid[x, (y + 1) % grid_height] == 1 and  # Below
                    grid[(x - 1) % grid_width, y] == 1 and  # Left
                    grid[(x + 1) % grid_width, y] == 1  # Right
            ):
                new_grid[x, y] = 1

    # Update the grid
    grid = np.copy(new_grid)

    # Draw the grid on the screen
    screen.fill(empty_color)
    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, wall_color, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()

