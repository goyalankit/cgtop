import curses
import curses.panel

from curses_helpers import create_window


class WindowInPanel:
    """Window in panel at the top with coordinates and size.

    This class creates a window based on attributes and adds
    them to the panel.

    Attributes:
        start_x: (int) x coordinate or column (curses).
        start_y: (int) y coordinate or row (curses).
        width: (int)  width of the box.
        height: (int) height of the box.
        panel: (`unicurses.panel`) panel object

    """

    def __init__(self, layout):
        self.layout = layout

        window = create_window(
            layout.start_x, layout.start_y, layout.width, layout.height
        )

        self.panel = curses.panel.new_panel(window)
        self.panel.top()


class StdScreen:
    def __init__(self):
        """Container for main screen.

        This class initializes the standard screen in unicurses and
        sets the maximum value for x and y coordinates.

        Attributes:
            stdscr: (`unicurses.stdscr`) initialized standard screen
            MAX_HEIGHT: (int) maximum value for y coordinate
            MAX_WIDTH: (int) maximum value for x coordinate

        """
        self.stdscr = curses.initscr()

        self.MAX_HEIGHT = self.stdscr.getmaxyx()[0] - 1
        self.MAX_WIDTH = self.stdscr.getmaxyx()[1] - 1

        curses.start_color()

    def disable_cursor_and_key_echo(self):
        curses.noecho()
        curses.curs_set(False)
        self.stdscr.keypad(True)


class Layout:
    def __init__(self, start_x, start_y, width, height, xy=None):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height

        self.xy = xy
