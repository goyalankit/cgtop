from unicurses import *

global_color_number = 1


def show_changes():
  """Update the panels to reflect the changes on screen."""
  update_panels()
  doupdate()


def create_window(start_x, start_y, width, height):
  """Create window helper method with sane parameter names."""
  return newwin(height, width, start_y, start_x)


def make_color(foreground, background):
  """Creates color on the fly with a unique id."""

  global global_color_number

  color_number = global_color_number
  init_pair(color_number, foreground, background)

  global_color_number += 1

  return color_number
