from src.logging.logger import Logger, ErrorLogger
from pathlib import Path

accepted_extensions = [
    ".txt",
    ".pdf",
    ".docx"
]

class ScanManager:
    Source: str
    files: list

    def __init__(self, source: str):
        self.Source = source
        if(self.Source.strip() == ""):
           ErrorLogger().error("ScanManager::__init__() : file/folder source is empty string")
           return 
        path = Path(self.Source)

        if(path.exists() == False):
            ErrorLogger().error("ScanManager::__init__() : file/folder does not exists")
            return 

        self.files = self.discover_files(path)
        if self.files == []:
            Logger().warning("ScanManager::__init__() : files array is empty, either path is not valid or no accepted_extension file found")

        
    def scan(self) -> list:
        result_list = []
        if self.files.__len__() == 0:
            Logger().warning("ScanManager::scan() : Nothing to scan, files list is empty")
            return [False]

        # call File Scanner for one time and give the whole array,
        # if single then loop runs for 1 time, if multiple then file runs multiple time
        return result_list

    def discover_files(self, path) -> list:
        files = []
        if path.is_file():
            if path.suffix.lower() in accepted_extensions:
                files.append(path)
                return files
        elif path.is_dir():
            paths = path.rglob("*")
            for p in paths:
                if p in accepted_extensions:
                    files.append(p)

            return files
        else:
            ErrorLogger().error("ScanManager::discover_files() : path is neither file nor direcotry")
        return []
