from constants import layout_grid
from utils import Layout

class LayoutCreator:
  def __init__(self, max_width, max_height, total):
    self.max_width = max_width
    self.max_height = max_height
    self.total = total


  def create_layouts(self):
    width_factor, height_factor = layout_grid[self.total]

    layouts = []

    curr_y = 0
    for y in xrange(height_factor):
      curr_x = 0

      for x in xrange(width_factor):
          layouts.append(
            Layout(
              curr_x, curr_y,
              self.max_width / width_factor, self.max_height / height_factor
            ))

          curr_x += self.max_width / width_factor + 1

      curr_y += self.max_height / height_factor + 1

    return layouts
