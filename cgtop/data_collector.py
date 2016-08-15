import cpu_sensor
import memory_sensor
import process_sensor

from curses_helpers import show_changes
from helpers import is_rh7
from update_heuristics import UpdateHeuristics


class DataCollector(object):
    def get_cpu_data(self, container):
        if is_rh7():
            return cpu_sensor.Rhel7CpuSensor(container).get_cpu_data()

        return cpu_sensor.Rhel6CpuSensor(container).get_cpu_data()

    def get_memory_data(self, container):
        if is_rh7():
            return memory_sensor.Rhel7MemorySensor(container).get_memory_data()

        return memory_sensor.Rhel6MemorySensor(container).get_memory_data()

    def get_process_data(self, container):
        if is_rh7():
            return process_sensor.Rhel7ProcessSensor(container).get_process_data()

        return process_sensor.Rhel6ProcessSensor(container).get_process_data()

    def consolidate_data(self, containers):
        data = {}
        for container in containers:
            data[container] = {}

            data[container].update(self.get_process_data(container))

            # CPU Data
            # data[container].update(self.get_cpu_data(container))

            # Memory Data
            data[container].update(self.get_memory_data(container))
        return data

    def update_widget_data(self, containers):
        UpdateHeuristics.tick()

        if UpdateHeuristics.skip_update():
            return

        data_for_container = self.consolidate_data(containers)
        for container in containers:
            data = data_for_container[container]

            # Disabling CPU bar until we have a good metric to show.

            # container.update_fill_bar_data(container.cpu_fill_bar,
            #                                new_data=data['fraction_cpu_usage'],
            #                                total_data=100,
            #                                start_text="CPU",
            #                                end_text="{0}/{1}".format(
            #                                    data['fraction_cpu_usage'], 100
            #                                ))

            container.update_fill_bar_data(container.memory_fill_bar,
                                           new_data=data['usage_in_bytes'],
                                           total_data=data['limit_in_bytes'],
                                           start_text="Mem",
                                           end_text="{0}/{1}".format(
                                               data['usage_in_bytes'],
                                               data['limit_in_bytes']
                                           ))

            if not container.process_list_bar.data_loaded:
                container.process_list_bar.set_output_lines(data['processes'])

        show_changes()
