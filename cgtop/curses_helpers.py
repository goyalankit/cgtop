import curses
from brownie.caching import memoize

global_color_number = 1


def show_changes():
    """Update the panels to reflect the changes on screen."""
    curses.panel.update_panels()
    curses.doupdate()


def create_window(start_x, start_y, width, height):
    """Create window helper method with sane parameter names."""
    return curses.newwin(height, width, start_y, start_x)


# It's critical that this method is memoized.
# Otherwise we will have color bleed.
# Either memoize of get rid of this method and
# provide colors as constants.
@memoize
def make_color(foreground, background):
    """Creates color on the fly with a unique id."""

    global global_color_number

    color_number = global_color_number
    curses.init_pair(color_number, foreground, background)

    global_color_number += 1

    return color_number
