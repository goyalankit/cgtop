from unicurses import *
from helpers import *


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


class StdScreen:
  def __init__(self):
    self.stdscr = initscr()

    self.MAX_HEIGHT = getmaxyx(self.stdscr)[0] - 1
    self.MAX_WIDTH = getmaxyx(self.stdscr)[1] - 1

    start_color()

  def disable_cursor_and_key_echo(self):
    noecho()
    curs_set(False)
    keypad(self.stdscr, True)


class Layout:
  def __init__(self, start_x, start_y, width, height):
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height