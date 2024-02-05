
def initialize_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

def update_grid(grid, x_cells, y_cells):
    new_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # Add logic to update the grid based on GoL rules
    # For now, this is just a placeholder
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            current_neighbours = check_neighbours(grid, x, y, x_cells, y_cells)
            if grid[y][x] == 1:
                if current_neighbours < 2:
                    new_grid[y][x] = 0
                elif current_neighbours > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if current_neighbours == 3:
                    new_grid[y][x] = 1
    return new_grid

def check_neighbours(grid, cell_x, cell_y, x_cells, y_cells):
    num_alive_neighbours = 0
    for x_offset in range(-1, 2):
        for y_offset in range(-1, 2):
            neighbor_x = cell_x + x_offset
            neighbor_y = cell_y + y_offset
            if not oob(neighbor_x, neighbor_y, x_cells, y_cells):
                if not (x_offset == 0 and y_offset == 0):
                    #if grid[cell_y][cell_x] == 1:
                        #print(f'Comparing cell at {cell_x}, {cell_y} with {neighbor_x} and {neighbor_y}')
                    if grid[neighbor_y][neighbor_x] == 1:
                        num_alive_neighbours += 1
    #print(num_alive_neighbours)
    return num_alive_neighbours


def oob(x, y, x_cells, y_cells):
    return x < 0 or x >= x_cells or y < 0 or y >= y_cells
