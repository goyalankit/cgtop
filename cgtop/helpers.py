from unicurses import *



def show_changes():
  update_panels()
  doupdate()


def create_window(start_x, start_y, width, height):
  return newwin(height, width, start_y, start_x)