"""
constants used throughout the application/
"""
ESC_KEY = 27
CHAR_Q = ord('q')

EXIT_KEYS = [ESC_KEY, CHAR_Q]

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

# TODO: Remove this once it's stable. We could simply abort
# on osx.

RHEL6_CGROUP_PATH = '/cgroup/lid'
RHEL7_CGROUP_PATH = '/sys/fs/cgroup'
CGROUP_DIRS = '/cgroup/lid'
