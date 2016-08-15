import os
import platform

from cgroup_container import CgroupContainer
from constants import CGROUP_DIRS
from curses_helpers import show_changes
from distutils.version import LooseVersion


# TODO: memoize this.
def get_current_cgroups():
    # TODO: remove hardcoded subsystem.
    subsystem_path = CGROUP_DIRS

    # TODO: Fix DUMMY DATA.
    if not subsystem_path or not os.path.exists(subsystem_path):
        return ['noop1', 'noop2', 'noop3', 'noop4', 'noop5',
                'noop6', 'noop7', 'noop8', 'noop9']

    return [item for item in os.listdir(subsystem_path) if
            os.path.isdir(os.path.join(subsystem_path, item))]


def create_app_containers(layouts, cgroup_names):
    containers = []

    # We want the layouts to be in order so that
    # we can use left and right arrows.
    required_layouts = layouts[0:len(cgroup_names)]
    cgroup_with_layouts = dict(zip(required_layouts, cgroup_names))

    for layout in required_layouts:
        cgroup_name = cgroup_with_layouts[layout]
        container = CgroupContainer(
            cgroup_name, cgroup_name, layout, cgroup_name
        )
        container.initialize_widgets()
        containers.append(container)

    show_changes()
    return containers


def read_metric_from_file(path):
    try:
        with open(path, 'rb') as fh:
            return fh.read().strip()
    except IOError:
        raise


def is_rh7():
    dist_name, dist_ver, _ = platform.dist()
    if dist_name.upper() == 'REDHAT':
        if LooseVersion(dist_ver) >= LooseVersion('7'):
            return True
    return False
