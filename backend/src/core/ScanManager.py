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
        self.files = []
        if(self.Source.strip() == ""):
           ErrorLogger().error("ScanManager::__init__() : file/folder source is empty string")
           return 
        path = Path(self.Source)

        if(path.exists() == False):
            ErrorLogger().error("ScanManager::__init__() : file/folder does not exists")
            return 

        if path.is_dir():
            Logger().info("ScanManager::__init__() : ${source} is a directory")
            self.files = [file for file in path.rglob("*") if file.is_file() and file.suffix.lower() in accepted_extensions]
        elif path.is_file():
            Logger().info("ScanManager::__init__() : ${source} is a file")
            if path.suffix.lower() in accepted_extensions:
                self.files = [path]
            else:
                Logger().warning("ScanManager::__init__() : ${source} is not accepted")    
                return 
        else:
            ErrorLogger().error("ScanManager::__init__() : ${source} is neither a file nor a directory")
            return

        
    def scan(self) -> list:
        success_list = []
        if self.files.__len__() == 0:
            Logger().warning("ScanManager::scan() : Nothing to scan, files list is empty")
            return [False]

        for file in self.files:
            

        # call File Scanner for every item in the files array,
        # if single then loop runs for 1 time, if multiple then file runs multiple time
        return success_list

