#!/usr/bin/env python

from cgroup_container import CgroupContainer
from constants import *
from utils import StdScreen, Layout
from unicurses import *
from helpers import *
from background_thread import BackgroundThread
import threading
import random
from layout_creator import LayoutCreator
from app_container import AppContainer

global_stop_event = threading.Event()


def update_my_data(containers):
  for cgroup_container in containers:
    data = random.randint(1, 100)
    cgroup_container.update_fill_bar_data(cgroup_container.cpu_fill_bar,
                                          new_data=data, total_data=100,
                                          start_text="CPU",
                                          end_text="%s/100" % data)

    cgroup_container.update_fill_bar_data(cgroup_container.memory_fill_bar,
                                          new_data=100,
                                          total_data=100, start_text="Mem",
                                          end_text="%s/200" % data)

  show_changes()


def main():
  stdscr = StdScreen()
  stdscr.disable_cursor_and_key_echo()

  lc = LayoutCreator(stdscr.MAX_WIDTH, stdscr.MAX_HEIGHT, 6)
  layouts = lc.create_layouts()
  containers = []
  for num, layout in enumerate(layouts):
    container = AppContainer("noop-app-i%s" % num, "/sys/fs/cgroup", layout, global_stop_event)
    container.initialize_bars()
    containers.append(container)

  show_changes()

  jb = BackgroundThread(update_my_data, global_stop_event, 1, containers)
  jb.start()

  start_event_loop()

  # End window.
  endwin()


def start_event_loop():
  running = True
  while running:
    key = getch()

    if key in [CHAR_Q, ESC_KEY]:
      global_stop_event.set()
      break


if __name__ == '__main__':
  main()
