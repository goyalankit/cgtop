"""
constants used throughout the application/
"""
import os
import platform

ESC_KEY = 27
CHAR_Q = ord('q')

# Data fetch interval time.
REFRESH_INTERVAL = 1.5

"""
Describes the way screen should be divides. There
may be a better way to do this, but this works fine
for the current application since all boxes are uniform.

{
  NUM_APPLICATIONS: [WIDTH_FACTOR, HEIGHT_FACTOR],
  ..
}

NUM_APPLICATIONS: number of applications
WIDTH_FACTOR: Parts in which width will be divided
HEIGHT_FACTOR: Parts in which height will be divided.

This assumes that most of the users are using landscape mode in
their screens.

TODO: autogenerate this thing.
"""
layout_grid = {
  1: [1, 1],
  2: [2, 2],
  3: [2, 2],
  4: [2, 2],
  5: [3, 2],
  6: [3, 2],
  7: [3, 3],
  8: [3, 3],
  9: [3, 3],
  10: [4, 3],
  11: [4, 3],
  12: [4, 3],
  13: [4, 4],
  14: [4, 4],
  15: [4, 4],
  16: [4, 4],
}

if os.environ.get('DEV') or platform.system() == 'Darwin':
  CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
  BASE_CGROUP_PATH = os.path.join(CURRENT_DIR, '../testdata/sys/fs/cgroup/')
else:
  # TODO: Differentiate between RHEL6 and RHEL7
  BASE_CGROUP_PATH = "/sys/fs/cgroup"
