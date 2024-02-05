
def initialize_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

def initialize_alive_cells(grid):
    """Initialize the set of alive cells based on the current grid."""
    return {(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 1}


def get_neighbors(x, y):
    """Generate all neighbor positions of a given cell."""
    return [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0)]

def update_grid(grid, alive_cells, x_cells, y_cells):
    new_alive_cells = set()
    potential_cells = set()

    # Find all potential cells to update (alive cells and their neighbors)
    for cell in alive_cells:
        potential_cells.add(cell)
        potential_cells.update(get_neighbors(*cell))

    # Filter potential cells to those within bounds
    potential_cells = {cell for cell in potential_cells if not oob(cell[0], cell[1], x_cells, y_cells)}

    new_grid = [[0 for _ in range(x_cells)] for _ in range(y_cells)]

    for cell in potential_cells:
        x, y = cell
        current_neighbours = check_neighbours(grid, x, y, x_cells, y_cells)
        if grid[y][x] == 1 and 2 <= current_neighbours <= 3:
            new_alive_cells.add((x, y))
            new_grid[y][x] = 1
        elif grid[y][x] == 0 and current_neighbours == 3:
            new_alive_cells.add((x, y))
            new_grid[y][x] = 1
    
    

    return new_grid, new_alive_cells

def check_neighbours(grid, cell_x, cell_y, x_cells, y_cells):
    num_alive_neighbours = 0
    for x_offset in range(-1, 2):
        for y_offset in range(-1, 2):
            neighbor_x = cell_x + x_offset
            neighbor_y = cell_y + y_offset
            if not oob(neighbor_x, neighbor_y, x_cells, y_cells):
                if not (x_offset == 0 and y_offset == 0):
                    if grid[neighbor_y][neighbor_x] == 1:
                        num_alive_neighbours += 1
    return num_alive_neighbours


def oob(x, y, x_cells, y_cells):
    return x < 0 or x >= x_cells or y < 0 or y >= y_cells
