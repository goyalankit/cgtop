#!/usr/bin/env python

from unicurses import *
from helpers import *
from colors import make_color


class FillBarPanel:
  def __init__(self, start_x, start_y, width, height):
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height

    window = create_window(start_x, start_y, width, height)
    panel = new_panel(window)
    top_panel(panel)
    self.panel = panel


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

  def update_fill_bar_data(self, fill_bar_panel, new_data, total_data,
                           start_text,
                           end_text):
    window = panel_window(fill_bar_panel.panel)
    wclear(window)

    # Add text like CPU, Mem
    waddstr(
      window, start_text,
      attr=color_pair(make_color(COLOR_CYAN, COLOR_BLACK))
    )

    # Add initial symbol
    waddstr(
      window, " [",
      attr=color_pair(make_color(COLOR_BLUE, COLOR_BLACK))
    )

    total_number_of_possible_bars = fill_bar_panel.width - len(start_text) - len(end_text) - 4

    percent_filled = int(new_data * total_number_of_possible_bars / total_data)
    filled_bars = "|" * percent_filled

    waddstr(
      window, filled_bars,
      attr=color_pair(make_color(COLOR_GREEN, COLOR_BLACK))
    )

    empty_space = " " * (total_number_of_possible_bars - percent_filled - 1)

    waddstr(window, empty_space)

    waddstr(window, "] ", attr=color_pair(make_color(COLOR_RED, COLOR_BLACK)))

    waddstr(window, end_text, attr=color_pair(make_color(COLOR_YELLOW, COLOR_BLACK)))

  def _create_fill_bar_panel(self, start_x, start_y, width, height):
    return FillBarPanel(start_x, start_y, width, height)

  def create_cpu_fill_bar(self):
    """Creates a cpu fill bar at the bottom of container.

    Coordinates:

    starts_x = x + 2
    start_y = max_y - 2
    width = total_width - 4
    height = 2

    :return: FillBarPanel object.
    """
    self.cpu_fill_bar = self._create_fill_bar_panel(
      self.start_x + 2, self.height - 2,
      self.width - 4, 1
    )

    return self.cpu_fill_bar

  def create_memory_fill_bar(self):
    # starts_x = x + 2
    # starts_y = max_y - (2 + 2 + 2)
    # width = total_width - 4
    # height = 2
    self.memory_fill_bar = self._create_fill_bar_panel(
      self.start_x + 2,
      self.height - 4,
      self.width - 4, 1)

    return self.memory_fill_bar


def main():
  stdscr = StdScreen()
  stdscr.disable_cursor_and_key_echo()

  # Need to store the panel in a variable to prevent
  # Garbage collection.
  cgroup_container = CgroupContainer(start_x=1, start_y=1,
                                     width=stdscr.MAX_WIDTH / 2,
                                     height=stdscr.MAX_HEIGHT / 2)
  cpu_fill_bar = cgroup_container.create_cpu_fill_bar()

  cgroup_container.update_fill_bar_data(cpu_fill_bar, new_data=10,
                                        total_data=100,
                                        start_text="CPU", end_text="120/200")

  memory_fill_bar = cgroup_container.create_memory_fill_bar()
  cgroup_container.update_fill_bar_data(memory_fill_bar, new_data=100,
                                        total_data=100,
                                        start_text="Mem", end_text="120/200")
  # # Progress Bar
  # fill_bar = newwin(2, max_x / 2 - 4, max_y/4 + 3, 2)
  # box(progress_bar)
  # progress_panel = new_panel(progress_bar)
  # wbkgd(progress_bar, '.', color_pair(make_color(COLOR_GREEN, COLOR_YELLOW)))
  # top_panel(progress_panel)

  show_changes()

  running = True
  i = 10
  while (running):
    # if i < max_x / 2 - 4:
    # progress_bar_progress = newwin(2, i + 1, max_y / 4 + 3, 2)
    # i += 2
    # box(progress_bar_progress)
    # wbkgd(progress_bar_progress, '.', color_pair(make_color(COLOR_GREEN, COLOR_RED)))
    # panel2 = new_panel(progress_bar_progress)
    # top_panel(panel2)
    # show_changes()
    if i <= 100:
      cgroup_container.update_fill_bar_data(cpu_fill_bar, new_data=i,
                                            total_data=100,
                                            start_text="CPU", end_text="%s/100" % i)
      i+=10
      show_changes()

    key = getch()
    if key == ord('q'):
      running = False
      break;

  # End window.
  endwin()


if __name__ == '__main__':
  main()
