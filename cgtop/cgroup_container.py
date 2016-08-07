from unicurses import *
from helpers import *
from utils import *


class CgroupContainer:
  def __init__(self, start_x, start_y, width, height, box_border=True):
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height
    self.window = create_window(start_x, start_y, width, height)

    self.cpu_fill_bar = None
    self.memory_fill_bar = None

    if box_border:
      box(self.window)
    self.main_panel = new_panel(self.window)

  @staticmethod
  def update_fill_bar_data(fill_bar_panel, new_data, total_data,
                           start_text,
                           end_text):
    window = panel_window(fill_bar_panel.panel)
    wclear(window)

    # Add text like CPU, Mem
    waddstr(
      window, start_text,
      attr=color_pair(make_color(COLOR_CYAN, COLOR_BLACK))
    )

    # Add initial symbol [
    waddstr(
      window, " [",
      attr=color_pair(make_color(COLOR_BLUE, COLOR_BLACK))
    )

    # Space for bars = total width - text and spacing.
    total_number_of_possible_bars = int(
      fill_bar_panel.width - len(start_text) - len(end_text) - 4
    )

    percent_filled_with_bars = int(
      new_data * total_number_of_possible_bars / total_data
    )

    filled_bars = "|" * percent_filled_with_bars

    # Add |'s to the progress bar
    waddstr(
      window, filled_bars,
      attr=color_pair(make_color(COLOR_GREEN, COLOR_BLACK))
    )

    empty_space = " " * (
      total_number_of_possible_bars - percent_filled_with_bars - 1
    )

    # Add empty space.
    waddstr(window, empty_space)

    # Add the ending/closing ']'
    waddstr(window, "] ", attr=color_pair(make_color(COLOR_RED, COLOR_BLACK)))

    # Add the end_text like 50/100%
    waddstr(window, end_text,
            attr=color_pair(make_color(COLOR_YELLOW, COLOR_BLACK)))

  def create_cpu_fill_bar(self):
    """Creates a cpu fill bar at the bottom of container.

    Coordinates:

    starts_x = x + 2
    start_y = max_y - 2
    width = total_width - 4
    height = 2

    :return: FillBarPanel object.
    """
    self.cpu_fill_bar = FillBarPanel(
      self.start_x + 2, self.height - 2,
      self.width - 4, 1
    )

    return self.cpu_fill_bar

  def create_memory_fill_bar(self):
    # starts_x = x + 2
    # starts_y = max_y - (2 + 2 + 2)
    # width = total_width - 4
    # height = 2
    self.memory_fill_bar = FillBarPanel(
      self.start_x + 2,
      self.height - 4,
      self.width - 4, 1)

    return self.memory_fill_bar
