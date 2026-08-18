from src.logging.logger import Logger, ErrorLogger

class FileScanner:
    paths: list

    def __init__(self, paths):
        self.paths = paths

    def start_scanning(self):
        