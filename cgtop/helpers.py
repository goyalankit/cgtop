from unicurses import *

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


def show_changes():
  update_panels()
  doupdate()


def create_window(start_x, start_y, width, height):
  return newwin(height, width, start_y, start_x)