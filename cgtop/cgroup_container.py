import curses

from curses_helpers import create_window, make_color
from models import WindowInPanel, Layout
from scrollable_list_widget import ScrollableListWidget


class CgroupContainer:
    """Base Container class per application.

    This class creates a container for an app with
    fill bars showing the current usage.
    """

    def __init__(self, name, cgpath, layout, title="CGroup Container"):
        # Dimensions.
        self.start_x = layout.start_x
        self.start_y = layout.start_y
        self.height = layout.height
        self.width = layout.width
        self.xy = layout.xy

        self.title = title
        self.name = name
        self.cgpath = cgpath

        # Main window for the container.
        self.window = create_window(
            self.start_x, self.start_y,
            self.width, self.height
        )

        self.main_panel = curses.panel.new_panel(self.window)
        self.title_panel = self.put_title_in_container(self.title)

        # We need this to prevent garbage collection.
        self.process_list_bar_panel = None

        self.cpu_fill_bar = None
        self.memory_fill_bar = None
        self.process_list_bar = None

    def initialize_widgets(self):
        """Create the initial fill bars for cpu and memory."""

        self.window.box()

        # Disabling CPU Bar until we have some good
        # metric to show here.

        # cpu_fill_bar = self.create_cpu_fill_bar()
        # self.update_fill_bar_data(
        #     cpu_fill_bar,
        #     new_data=0, total_data=100,
        #     start_text="CPU", end_text="0/0"
        # )

        memory_fill_bar = self.create_memory_fill_bar()
        self.update_fill_bar_data(
            memory_fill_bar,
            new_data=0, total_data=100,
            start_text="Mem", end_text="0/0"
        )

        self.process_list_bar = self.create_process_list_bar()

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

        window = fill_bar_panel.panel.window()
        window.erase()

        # Add text like CPU, Mem
        window.addstr(
            0, 0, start_text,
            curses.color_pair(make_color(curses.COLOR_CYAN, curses.COLOR_BLACK))
        )

        # Add initial symbol [
        window.addstr(
            " [",
            curses.color_pair(make_color(curses.COLOR_RED, curses.COLOR_BLACK))
        )

        # Space for bars = total width - text and spacing.
        total_number_of_possible_bars = int(
            fill_bar_panel.layout.width - len(start_text) - len(end_text) - 6
        )

        percent_filled_with_bars = int(
            new_data * total_number_of_possible_bars / total_data
        )

        filled_bars = "|" * percent_filled_with_bars

        # Add |'s to the progress bar
        window.addstr(
            filled_bars,
            curses.color_pair(make_color(curses.COLOR_GREEN, curses.COLOR_BLACK))
        )

        empty_space = " " * (
            total_number_of_possible_bars - percent_filled_with_bars - 1
        )

        # Add empty space.
        window.addstr(empty_space)

        # Add the ending/closing ']'
        window.addstr(
            "] ",
            curses.color_pair(make_color(curses.COLOR_RED, curses.COLOR_BLACK))
        )

        # Add the end_text like 50/100%
        window.addstr(
            end_text,
            curses.color_pair(make_color(curses.COLOR_YELLOW, curses.COLOR_BLACK))
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
        self.cpu_fill_bar = WindowInPanel(
            Layout(
                self.start_x + 2, self.start_y + self.height - 2,
                self.width - 4, 1
            ))

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
        self.memory_fill_bar = WindowInPanel(
            Layout(
                self.start_x + 2, self.start_y + self.height - 4,
                self.width - 4, 1
            ))

        return self.memory_fill_bar

    def put_title_in_container(self, title=None):
        """Set title of the container.

        :param title: Text to be set as title
        :return: None
        """
        if title is not None:
            self.title = title

        t_start_x = self.start_x + (self.width - len(self.title)) / 2

        window = create_window(
            t_start_x, self.start_y + 1,
            len(self.title) + 2, 1
        )

        window.addstr(self.title)
        return curses.panel.new_panel(window)

    def create_process_list_bar(self):

        reserve_height = 4  # For things above the process bar.
        process_bar_height = self.height - 4 - reserve_height - 2

        self.process_list_bar_panel = WindowInPanel(
            Layout(
                self.start_x + 2,
                self.start_y + self.height - process_bar_height - 4,
                self.width - 4,
                process_bar_height)
        )
        self.process_list_bar_panel.panel.window().box()
        self.process_list_bar = ScrollableListWidget(
            self.process_list_bar_panel.panel.window(),
            self.width, process_bar_height - 2
        )

        return self.process_list_bar
