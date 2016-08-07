#!/usr/bin/env python

from cgroup_container import CgroupContainer
from utils import StdScreen
from unicurses import *
from helpers import show_changes


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
