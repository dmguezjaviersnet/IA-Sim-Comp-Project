class Logger:
    def __init__(self):
        self.errors_list = []

    def add_error(self, error_name: str):
        self.errors_list.append(error_name)