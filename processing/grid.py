import math

from opensimplex import OpenSimplex


class Grid:
    """Abstraction for Grid Object.

    Attributes:
        width <int>: width dimension for grid
        height <int>: width dimension for grid
    """
    def __init__(self, width, height, rez):
        self.width = width
        self.height = height
        self.rez = rez

        self.rows = self.width / self.rez
        self.cols = self.height / self.rez
        self.grid = [[0] * self.cols for _ in xrange(self.rows)]

        self.noise = OpenSimplex()
        self.z = 0

    def fill_grid(self):
        """Fill the grid using OpenSimplex Noise.

        This function fills each element of the grid using a specific function
        for randomness.
        """
        x_y_inc = 0.1
        z_inc = 0.1
        x = 0
        for row in xrange(self.rows):
            x += x_y_inc
            y = 0
            for col in xrange(self.cols):
                self.grid[row][col] = self.noise.noise3d(
                    x, y, self.z
                )
                y += x_y_inc
        self.z += z_inc

    def draw_grid(self):
        """Display grid on screen"""
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                fill(self.grid[i][j]*255)
                noStroke()
                rect(i*self.rez, j*self.rez, self.rez, self.rez)

    def draw_vectors(self):
        """Draw vectors for each unit in the grid"""
        for i in xrange(self.rows - 1):
            for j in xrange(self.cols - 1):
                x = i * self.rez
                y = j * self.rez
                # Defining mid-points for the unit
                vector_a = (x + self.rez * 0.5, y)
                vector_b = (x + self.rez, y + self.rez * 0.5)
                vector_c = (x + self.rez * 0.5, y + self.rez)
                vector_d = (x, y + self.rez * 0.5)

                switch = {
                    1: [(vector_c, vector_d)],
                    2: [(vector_b, vector_c)],
                    3: [(vector_b, vector_d)],
                    4: [(vector_a, vector_b)],
                    5: [(vector_a, vector_d), (vector_b, vector_c)],
                    6: [(vector_a, vector_c)],
                    7: [(vector_a, vector_d)],
                    8: [(vector_a, vector_d)],
                    9: [(vector_a, vector_c)],
                    10: [(vector_a, vector_b), (vector_c, vector_d)],
                    11: [(vector_a, vector_b)],
                    12: [(vector_b, vector_d)],
                    13: [(vector_b, vector_c)],
                    14: [(vector_c, vector_d)],
                }

                state = abs(self._get_state(i, j))
                stroke(255)
                strokeWeight(1)

                for config in switch.get(state, []):
                    self.line(*config)


    def line(self, v1, v2):
        """Naive overload for drawing a line that join vectors"""
        line(v1[0], v1[1], v2[0], v2[1])

    def _get_state(self, x, y):
        """Returns the state for the unit.

        The state is the binary representation of the vectors and is used to
        map back to a particular unit for drawing the lines.
        """
        return (
            math.ceil(self.grid[x][y+1]) * 1 +
            math.ceil(self.grid[x+1][y+1]) * 2 +
            math.ceil(self.grid[x+1][y]) * 4 +
            math.ceil(self.grid[x][y]) * 8
        )
