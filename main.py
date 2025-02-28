import math
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon


class Hexagon:
    def __init__(self, center_x, center_y, side_length):
        self.grid_center_x = center_x
        self.grid_center_y = center_y
        self.coordinate_center_x = side_length * math.sqrt(3) * center_x
        if center_y % 2 == 1:
            self.coordinate_center_x += side_length * math.sqrt(3)/2
        self.coordinate_center_y = side_length * 3/2 * center_y
        self.side_length = side_length

        # convert from millimeters to inches for matplotlib
        self.coordinate_center_x /= 25.4
        self.coordinate_center_y /= 25.4
        self.side_length /= 25.4

    def draw_hexagon(self, axis):
        hexagon = RegularPolygon((self.coordinate_center_x, self.coordinate_center_y), numVertices=6, radius=self.side_length, edgecolor='Blue', fill=False)
        axis.add_patch(hexagon)


triangle_side_length = 2.5  # in millimeters

overall_width = 100  # 10 centimeters in millimeters
overall_height = 100  # 10 centimeters in millimeters

num_hexagons_wide = 2 + math.ceil(overall_width / (2 * math.sqrt(3)*triangle_side_length))
num_hexagons_tall = 2 + math.ceil(overall_height / (2 * math.sqrt(3)*triangle_side_length))

hexagon_grid = [[Hexagon(idx, jdx, 2*triangle_side_length) for jdx in range(num_hexagons_tall)] for idx in range(num_hexagons_wide)]

plt.rcParams['figure.figsize'] = overall_width/25.4, overall_height/25.4
ax = plt.gca()
ax.set_xlim([0, overall_width/25.4])
ax.set_ylim([0, overall_height/25.4])

for idx in range(num_hexagons_wide):
    for jdx in range(num_hexagons_tall):
        hexagon_grid[idx][jdx].draw_hexagon(ax)
plt.axis('off')
plt.savefig('pic.png', bbox_inches='tight', pad_inches=0)
