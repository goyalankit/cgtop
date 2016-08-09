#!/usr/bin/env python

from background_thread import BackgroundThread
from constants import EXIT_KEYS, REFRESH_INTERVAL
from data_fetcher import DataFetcher
from helpers import create_app_containers
from layout_creator import LayoutCreator
from models import StdScreen
from unicurses import endwin, getch


def top():
    standard_screen = StdScreen()
    standard_screen.disable_cursor_and_key_echo()

    lc = LayoutCreator(standard_screen.MAX_WIDTH, standard_screen.MAX_HEIGHT)
    layouts = lc.create_layouts()

    containers = create_app_containers(layouts, lc.cgroup_names)

    # Thread to periodically fetch data
    # and update the view.
    data_updater = BackgroundThread(
        DataFetcher().update_my_data,
        REFRESH_INTERVAL, containers
    )

    data_updater.start()

    # Wait forever until we receive
    # an exit key.
    while not getch() in EXIT_KEYS:
        pass

    data_updater.stop()

    endwin()


if __name__ == '__main__':
    top()
