import os

from app_container import AppContainer
from brownie.caching import memoize
from constants import BASE_CGROUP_PATH
from unicurses_helpers import show_changes


@memoize
def get_current_cgroups():
    # TODO: remove hardcoded subsystem.
    subsystem_path = BASE_CGROUP_PATH + "memory"

    # TODO: Fix DUMMY DATA.
    if not os.path.exists(subsystem_path):
        return ['noop1', 'noop2', 'noop3', 'noop4']

    return [item for item in os.listdir(subsystem_path) if
            os.path.isdir(os.path.join(subsystem_path, item))]


def create_app_containers(layouts, cgroup_names):
    containers = []
    cgroup_with_layouts = dict(zip(cgroup_names, layouts))

    for cgroup_name, layout in cgroup_with_layouts.iteritems():
        container = AppContainer(cgroup_name, cgroup_name, layout)
        container.initialize_bars()

        containers.append(container)

    show_changes()
    return containers


def read_metric_from_file(path):
    try:
        with open(path, 'rb') as fh:
            return fh.read().strip()
    except IOError:
        raise
