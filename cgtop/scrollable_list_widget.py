import curses
from curses_helpers import make_color


class ScrollableListWidget:
    DOWN = 1
    UP = -1

    def __init__(self, window, width, height):
        self.window = window

        self.width = width
        self.height = height

        self.top_line_num = 1
        self.highlight_line_num = 1

        self.output_lines = ['Loading process data ...']
        self.num_output_lines = 1
        self.data_loaded = False

        self.highlight = False

    def dispatch(self, c):
        if c == curses.KEY_UP:
            self.updown(self.UP)
        elif c == curses.KEY_DOWN:
            self.updown(self.DOWN)

        self.display_window()

    def set_output_lines(self, output_lines):
        """Method that adds the lines to be shown."""
        self.data_loaded = True
        self.output_lines = output_lines
        self.num_output_lines = len(self.output_lines)
        self.display_window()

    def set_highlight(self, highlight):
        self.highlight = highlight
        self.display_window()

    def display_window(self):

        # Clean the window to redraw
        self.window.clear()
        self.window.box()

        top = self.top_line_num - 1
        bottom = self.top_line_num + self.height - 1
        self.window.addstr("{num} processes.".format(num=self.num_output_lines))
        for (index, line,) in enumerate(self.output_lines[top:bottom]):
            index += 1

            # highlight current line
            if index != self.highlight_line_num:
                self.window.addnstr(index, 2, line, self.width - 5)
            else:
                color = 0
                if self.highlight:
                    color = curses.color_pair(make_color(curses.COLOR_RED, curses.COLOR_YELLOW))

                self.window.addnstr(index, 2, line, self.width - 5, color)

        self.window.refresh()

    # move highlight up/down one line
    def updown(self, increment):

        next_line_num = self.highlight_line_num + increment

        if increment == self.UP:
            # The highlighted row is at the top but it's not the topmost
            if self.highlight_line_num == 1 and self.top_line_num != 1:
                self.top_line_num += self.UP
                return

            # Highlight row is not at the top, so make upper row highlight.
            elif self.top_line_num != 1 or self.highlight_line_num != 1:
                self.highlight_line_num = next_line_num

        elif increment == self.DOWN:
            if next_line_num == self.height + 1 and (self.top_line_num + self.height + 1) != self.num_output_lines:
                self.top_line_num += self.DOWN
                return

            elif ((self.top_line_num + self.highlight_line_num + 1) != self.num_output_lines
                  and self.highlight_line_num != self.height):

                self.highlight_line_num = next_line_num
