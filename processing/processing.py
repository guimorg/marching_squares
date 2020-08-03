from grid import Grid

REZ = 5
grid = noise = None


def setup():
    global REZ, grid
    # fullScreen(P2D)
    noSmooth()
    size(256, 224, FX2D)
    grid = Grid(
        width=width, height=height, rez=REZ
    )


def draw():
    global grid
    background(0)
    grid.fill_grid()
    grid.draw_grid()
    grid.draw_vectors()
