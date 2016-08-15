from background_thread import BackgroundThread
from constants import REFRESH_INTERVAL, EXIT_KEYS
from curses import endwin, delay_output, KEY_RIGHT, KEY_UP, KEY_DOWN
from data_collector import DataCollector
from helpers import create_app_containers
from layout_creator import LayoutCreator
from models import StdScreen
from update_heuristics import UpdateHeuristics


def top():
    standard_screen = StdScreen()
    standard_screen.disable_cursor_and_key_echo()

    lc = LayoutCreator(standard_screen.MAX_WIDTH, standard_screen.MAX_HEIGHT)
    layouts = lc.create_layouts()

    containers = create_app_containers(layouts, lc.cgroup_names)

    # Thread to periodically fetch data
    # and update the view.
    data_updater = BackgroundThread(
        DataCollector().update_widget_data,
        REFRESH_INTERVAL, containers
    )
    data_updater.start()

    # Prevents used from bombarding with
    # key events.
    delay_output(1000)

    current_hightlight = containers[0]
    # Wait forever until we receive
    containers[0].process_list_bar.set_highlight(True)
    # an exit key.
    try:
        while True:
            key = standard_screen.stdscr.getch()
            if key in EXIT_KEYS:
                break

            current_hightlight = dispatch_to_container(containers, current_hightlight, key)

        data_updater.stop()

        endwin()
    except Exception:
        raise


def dispatch_to_container(containers, current_highlight, key):
    """Dispatch the key to container and handle highlighting.

    If the LEFT or RIGHT key is pressed, we switch the highlighting
    to the next container.

    """
    if key in [KEY_RIGHT]:
        next_true = False
        UpdateHeuristics.force_unupdate()
        current_highlight.process_list_bar.set_highlight(False)
        for container in containers:
            if next_true:
                next_true = False
                current_highlight = container
                break

            if container == current_highlight:
                next_true = True

        if next_true:
            current_highlight = containers[0]

        current_highlight.process_list_bar.set_highlight(True)
    elif key in [KEY_UP, KEY_DOWN]:
        UpdateHeuristics.force_unupdate()
        current_highlight.process_list_bar.dispatch(key)

    return current_highlight

if __name__ == '__main__':
    top()
