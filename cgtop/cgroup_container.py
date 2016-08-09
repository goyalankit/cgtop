import unicurses as uc

from unicurses_helpers import create_window, make_color
from models import FillBarPanel


class CgroupContainer:
    """Base Container class per application

    This class creates a container for an app with
    fill bars showing the current usage.
    """

    def __init__(self, layout, box_border=True,
                 title="CGroup Container"):
        self.start_x = layout.start_x
        self.start_y = layout.start_y
        self.width = layout.width
        self.height = layout.height

        self.window = create_window(
            self.start_x, self.start_y,
            self.width, self.height
        )

        self.title = title

        self.cpu_fill_bar = None
        self.memory_fill_bar = None

        if box_border:
            uc.box(self.window)

        self.main_panel = uc.new_panel(self.window)
        self.title_panel = None
        self.cpu_fill_bar = None
        self.memory_fill_bar = None

    @staticmethod
    def update_fill_bar_data(fill_bar_panel, new_data, total_data,
                             start_text, end_text):
        """
        Update the data in fill.

        :param fill_bar_panel: panel object for the fill bar.
        :param new_data: updated value of the metric.
        :param total_data: Max value of the metric.
        :param start_text: Description before fill bar
        :param end_text: Display something at the end of bar.

        :return:
        """
        window = uc.panel_window(fill_bar_panel.panel)
        uc.wclear(window)

        # Add text like CPU, Mem
        uc.waddstr(
            window, start_text,
            attr=uc.color_pair(make_color(uc.COLOR_CYAN, uc.COLOR_BLACK))
        )

        # Add initial symbol [
        uc.waddstr(
            window, " [",
            attr=uc.color_pair(make_color(uc.COLOR_BLUE, uc.COLOR_BLACK))
        )

        # Space for bars = total width - text and spacing.
        total_number_of_possible_bars = int(
            fill_bar_panel.width - len(start_text) - len(end_text) - 4
        )

        percent_filled_with_bars = int(
            new_data * total_number_of_possible_bars / total_data
        )

        filled_bars = "|" * percent_filled_with_bars

        # Add |'s to the progress bar
        uc.waddstr(
            window, filled_bars,
            attr=uc.color_pair(make_color(uc.COLOR_GREEN, uc.COLOR_BLACK))
        )

        empty_space = " " * (
            total_number_of_possible_bars - percent_filled_with_bars - 1
        )

        # Add empty space.
        uc.waddstr(window, empty_space)

        # Add the ending/closing ']'
        uc.waddstr(
            window, "] ",
            attr=uc.color_pair(make_color(uc.COLOR_RED, uc.COLOR_BLACK))
        )

        # Add the end_text like 50/100%
        uc.waddstr(
            window, end_text,
            attr=uc.color_pair(make_color(uc.COLOR_YELLOW, uc.COLOR_BLACK))
        )

    def create_cpu_fill_bar(self):
        """Creates a cpu fill bar at the bottom of container.

        Coordinates:

        starts_x = x + 2
        start_y = max_y - 2
        width = total_width - 4
        height = 2

        :return: FillBarPanel object.
        """
        self.cpu_fill_bar = FillBarPanel(
            self.start_x + 2, self.start_y + self.height - 2,
            self.width - 4, 1
        )

        return self.cpu_fill_bar

    def create_memory_fill_bar(self):
        """Creates a memory fill bar at the bottom of container.

        Coordinates:

        starts_x = x + 2
        start_y = max_y - 2
        width = total_width - 4
        height = 2

        :return: FillBarPanel object.
        """
        self.memory_fill_bar = FillBarPanel(
            self.start_x + 2,
            self.start_y + self.height - 4,
            self.width - 4, 1)

        return self.memory_fill_bar

    def title_window_on_screen(self, title=None):
        """Set title of the container.

        :param title: Text to be set as title
        :return: None
        """
        if title is not None:
            self.title = title

        t_start_x = self.start_x + (self.width - len(self.title)) / 2
        window = create_window(t_start_x, self.start_y + 1, len(self.title) + 2,
                               1)
        uc.waddstr(window, self.title)
        self.title_panel = uc.new_panel(window)
