#!/usr/bin/env python

from cgroup_container import CgroupContainer
from constants import *
from utils import StdScreen, Layout
from unicurses import *
from background_thread import BackgroundThread
import threading
import random
from layout_creator import LayoutCreator

global_stop_event = threading.Event()


def update_my_data(cgroup_container):
  data = random.randint(1, 100)
  cgroup_container.update_fill_bar_data(cgroup_container.cpu_fill_bar,
                                        new_data=data, total_data=100,
                                        start_text="CPU",
                                        end_text="%s/100" % data)


def main():
  stdscr = StdScreen()
  stdscr.disable_cursor_and_key_echo()

  lc = LayoutCreator(stdscr.MAX_WIDTH, stdscr.MAX_HEIGHT, 12)
  layouts = lc.create_layouts()

  for layout in layouts:
  # Need to store the panel in a variable to prevent
  # Garbage collection.
  #layout = Layout(start_x=1, start_y=1,
  #                width=stdscr.MAX_WIDTH / 3,
  #                height=stdscr.MAX_HEIGHT / 2)

    cgroup_container = CgroupContainer(layout)
    cgroup_container.title_window_on_screen()
    cpu_fill_bar = cgroup_container.create_cpu_fill_bar()

    cgroup_container.update_fill_bar_data(cpu_fill_bar, new_data=10,
                                          total_data=100,
                                          start_text="CPU", end_text="120/200")

    memory_fill_bar = cgroup_container.create_memory_fill_bar()
    cgroup_container.update_fill_bar_data(memory_fill_bar, new_data=100,
                                          total_data=100,
                                          start_text="Mem", end_text="120/200")

    jb = BackgroundThread(update_my_data, global_stop_event, 1, cgroup_container)
    jb.start()


  running = True
  while running:
    key = getch()

    if key in [CHAR_Q, ESC_KEY]:
      global_stop_event.set()
      break

  # End window.
  endwin()


if __name__ == '__main__':
  main()
