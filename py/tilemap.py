# py/tilemap.py

# Tile IDs
FLOOR = 0   # limestone - walkable
WALL  = 1   # stone - collision
EDGE  = 2   # stone frame - collision (wall border)
VOID  = 3   # empty/dark - collision (outside cave)

def build_cave_map(world_cols, world_rows):
    """Returns (tile_grid, collision_set)"""
    grid = [[VOID] * world_rows for _ in range(world_cols)]

    # Carve out a simple starter cave room roughly centered
    # Outer walls
    for x in range(44, 66):
        for y in range(44, 62):
            grid[x][y] = WALL

    # Inner floor
    for x in range(46, 64):
        for y in range(46, 60):
            grid[x][y] = FLOOR

    # Edge/border tiles on the wall perimeter
    for x in range(45, 65):
        grid[x][45] = EDGE
        grid[x][59] = EDGE
    for y in range(45, 60):
        grid[45][y] = EDGE
        grid[64][y] = EDGE

    # Build collision set from non-floor tiles
    collision = set()
    for x in range(world_cols):
        for y in range(world_rows):
            if grid[x][y] != FLOOR:
                collision.add((x, y))

    return grid, collision
