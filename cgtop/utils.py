import unicurses as uc

from helpers import create_window


class FillBarPanel:
  def __init__(self, start_x, start_y, width, height):
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height

    window = create_window(start_x, start_y, width, height)
    panel = uc.new_panel(window)
    uc.top_panel(panel)
    self.panel = panel


class StdScreen:
  def __init__(self):
    self.stdscr = uc.initscr()

    self.MAX_HEIGHT = uc.getmaxyx(self.stdscr)[0] - 1
    self.MAX_WIDTH = uc.getmaxyx(self.stdscr)[1] - 1

    uc.start_color()

  def disable_cursor_and_key_echo(self):
    uc.noecho()
    uc.curs_set(False)
    uc.keypad(self.stdscr, True)


class Layout:
  def __init__(self, start_x, start_y, width, height):
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height