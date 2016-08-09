from cgroup_container import CgroupContainer


class AppContainer(CgroupContainer):
    def __init__(self, name, cgpath, layout):
        CgroupContainer.__init__(self, layout, title=name)

        self.name = name
        self.cgpath = cgpath

    def initialize_bars(self):
        self.title_window_on_screen()

        cpu_fill_bar = self.create_cpu_fill_bar()
        self.update_fill_bar_data(
            cpu_fill_bar,
            new_data=0, total_data=100,
            start_text="CPU", end_text="0/0"
        )

        memory_fill_bar = self.create_memory_fill_bar()
        self.update_fill_bar_data(
            memory_fill_bar,
            new_data=0, total_data=100,
            start_text="Mem", end_text="0/0"
        )
