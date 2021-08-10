import os

class IterationManager:

    def __init__(self):
        self._task_number = None
        self._iteration_size = None
        self._start = None
        self._end = None
        # self._project_name = None
        self._results_path = None
        # self.results_file_headers = None  # TODO: Not sure if needed

    @property
    def task_number(self):
        return self._task_number

    @task_number.setter
    def task_number(self, value):
        self._task_number = value

    @property
    def iteration_size(self):
        return self._iteration_size

    @iteration_size.setter
    def iteration_size(self, value):
        self._iteration_size = int(value if value >= 0 else 0)
        self._start = None
        self._end = None

    @property
    def start(self):
        if self._start is None:
            self._start = self.task_number * self.iteration_size
        return self._start

    @property
    def end(self):
        if self._end is None:
            self._end = (self.task_number + 1) * self.iteration_size
        return self._end

    # @property
    # def project_name(self):
    #     return self._project_name
    #
    # @project_name.setter
    # def project_name(self, name):
    #     self._project_name = name
    #     # TODO: validate name

    @property
    def results_path(self):
        return self._results_path

    @results_path.setter
    def results_path(self, path):
        # TODO: raise error
        os.makedirs(path)
        # TODO validate path
        # TODO: set path according to project name
        self._results_path = path
