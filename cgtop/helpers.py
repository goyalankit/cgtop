import os
import unicurses as uc

global_color_number = 1


def show_changes():
  """Update the panels to reflect the changes on screen."""
  uc.update_panels()
  uc.doupdate()


def create_window(start_x, start_y, width, height):
  """Create window helper method with sane parameter names."""
  return uc.newwin(height, width, start_y, start_x)


def make_color(foreground, background):
  """Creates color on the fly with a unique id."""

  global global_color_number

  color_number = global_color_number
  uc.init_pair(color_number, foreground, background)

  global_color_number += 1

  return color_number


def read_metric_from_file(path):
  try:
    with open(path, 'rb') as fh:
      return fh.read().strip()
  except IOError:
    raise


# TODO memoize this method.
# TODO remove hardcoded subsystem.
def get_current_cgroups():
  subsystem_path = "/Users/angoyal/ws/code/extras/cgtop/testdata/sys/fs/cgroup/memory"
  cgroup_names = [item for item in os.listdir(subsystem_path) if
                  os.path.isdir(os.path.join(subsystem_path, item))]
  return cgroup_names
