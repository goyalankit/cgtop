#!/usr/bin/env python

import threading

from app_container import AppContainer
from background_thread import BackgroundThread
from constants import CHAR_Q, ESC_KEY, REFRESH_INTERVAL
from data_fetcher import DataFetcher
from layout_creator import LayoutCreator
from unicurses import endwin, getch
from utils import StdScreen

global_stop_event = threading.Event()


def main():
  standard_screen = StdScreen()
  standard_screen.disable_cursor_and_key_echo()

  lc = LayoutCreator(standard_screen.MAX_WIDTH, standard_screen.MAX_HEIGHT)
  layouts = lc.create_layouts()

  # Thread to periodically fetch data
  # and update the view.
  bt = BackgroundThread(
    DataFetcher().update_my_data,
    global_stop_event, REFRESH_INTERVAL,
    AppContainer.create_app_containers(
      layouts,
      global_stop_event
    )
  )

  bt.start()

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
