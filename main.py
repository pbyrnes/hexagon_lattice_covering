import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, RegularPolygon


def get_diamond_color(diamond):
    if math.isclose(diamond[1][0], diamond[3][0]):
        return 'red'
    if (diamond[1][0] - diamond[3][0]) * (diamond[1][1] - diamond[3][1]) > 0:
        return 'green'
    return 'yellow'


class Hexagon:
    def __init__(self, center_x, center_y, side_length):
        self.grid_center_x = center_x
        self.grid_center_y = center_y
        self.coordinate_center_x = side_length * math.sqrt(3) * center_x
        if center_y % 2 == 1:
            self.coordinate_center_x += side_length * math.sqrt(3)/2
        self.coordinate_center_y = side_length * 3/2 * center_y
        self.side_length = side_length
        self.diamonds = self.get_diamond_tiling()

    def get_diamond_tiling(self):
        triangles = (
            {(-2, 0), (-1, 0), (-1, -1)},
            {(-2, 0), (-1, 0), (-2, 1)},
            {(-1, 0), (-2, 1), (-1, 1)},
            {(-2, 1), (-1, 1), (-2, 2)},
            {(-2, 2), (-1, 1), (-1, 2)},
            {(0, -2), (0, -1), (-1, -1)},
            {(-1, -1), (0, -1), (-1, 0)},
            {(-1, 0), (0, -1), (0, 0)},
            {(-1, 0), (0, 0), (-1, 1)},
            {(-1, 1), (0, 0), (0, 1)},
            {(-1, 1), (0, 1), (-1, 2)},
            {(-1, 2), (0, 1), (0, 2)},
            {(0, -2), (1, -2), (0, -1)},
            {(1, -2), (0, -1), (1, -1)},
            {(0, -1), (1, -1), (0, 0)},
            {(1, -1), (0, 0), (1, 0)},
            {(0, 0), (1, 0), (0, 1)},
            {(1, 0), (0, 1), (1, 1)},
            {(0, 1), (1, 1), (0, 2)},
            {(1, -2), (2, -2), (1, -1)},
            {(2, -2), (1, -1), (2, -1)},
            {(1, -1), (2, -1), (1, 0)},
            {(2, -1), (1, 0), (2, 0)},
            {(1, 0), (2, 0), (1, 1)},
        )
        diamond_indices = [
            (0, 6),
            (1, 2),
            (3, 4),
            (5, 12),
            (7, 8),
            (9, 16),
            (10, 11),
            (13, 14),
            (15, 21),
            (17, 18),
            (19, 20),
            (22, 23),
        ]
        diamonds = []
        for a, b in diamond_indices:
            triangle_1 = triangles[a]
            triangle_2 = triangles[b]
            shared_vertices = triangle_1.intersection(triangle_2)
            if len(shared_vertices) != 2:
                raise ValueError(f'triangles in diamond do not share 2 vertices. {triangle_1=}, {triangle_2=}, {a=}, {b=}')
            v1 = list(triangle_1.difference(shared_vertices))[0]
            v2, v4 = list(shared_vertices)
            v3 = list(triangle_2.difference(shared_vertices))[0]
            diamonds.append(tuple(self.convert_coordinates_relative_to_actual(v) for v in [v1, v2, v3, v4]))
        return diamonds

    def convert_coordinates_relative_to_actual(self, v):
        x, y = v
        return self.coordinate_center_x + (x+y) * math.sqrt(3)/2 * self.side_length/2, self.coordinate_center_y + (y-x) * 1/2 * self.side_length/2

    def draw_hexagon(self, axis):
        hexagon = RegularPolygon((self.coordinate_center_x, self.coordinate_center_y), numVertices=6, radius=self.side_length, edgecolor='Blue', fill=False, linewidth=0.3)
        axis.add_patch(hexagon)

    def draw_hexagon_diamond_tiling(self, axis):
        for diamond in self.diamonds:
            color = get_diamond_color(diamond)
            diamond_patch = Polygon(diamond, edgecolor=None, facecolor=color)
            axis.add_patch(diamond_patch)


triangle_side_length = 2.5 / 25.4  # in inches (to support matplotlib)

overall_width = 10 / 2.54  # in inches
overall_height = 10 / 2.54  # in inches

num_hexagons_wide = 1 + math.ceil(overall_width / (2 * math.sqrt(3)*triangle_side_length))
num_hexagons_tall = 1 + math.ceil(overall_height / (3 * triangle_side_length))

hexagon_grid = [[Hexagon(idx, jdx, 2*triangle_side_length) for jdx in range(num_hexagons_tall)] for idx in range(num_hexagons_wide)]

plt.rcParams['figure.figsize'] = overall_width, overall_height
ax = plt.gca()
ax.set_xlim([0, overall_width])
ax.set_ylim([0, overall_height])

for idx in range(num_hexagons_wide):
    for jdx in range(num_hexagons_tall):
        hexagon_grid[idx][jdx].draw_hexagon_diamond_tiling(ax)
        hexagon_grid[idx][jdx].draw_hexagon(ax)
plt.axis('off')
plt.savefig('pic.png', bbox_inches='tight', pad_inches=0, dpi=1200)
