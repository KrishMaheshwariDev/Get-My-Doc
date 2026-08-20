from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.logging.logger import Logger, ErrorLogger
from backend.src.logging import CusException

@dataclass
class FileInfo:
    path: str
    filename: str
    extension: str
    size_bytes: int
    created_at: str
    modified_at: str
    content_hash: str


class FileScanner:
    SUPPORTED_EXTENTIONS = {
        ".pdf",
        ".txt",
        ".docx",
        ".ppt"
    }

# scan function takes the path and create an array of scannable files
    def scan(self, path: str) -> list[FileInfo]:
        Logger.info(f"Starting scan: {path}")
        scannable_files = []
        root = Path(path)
        scanned_files_info = []
        try:
            if not root.exists():
                raise FileNotFoundError(f"Path does not exists: {path}")

            if root.is_dir():
                scannable_files = self.traverse_directory(root)
            elif root.is_file():
                if root.suffix.lower() in self.SUPPORTED_EXTENTIONS:
                    scannable_files = [root]
                else:
                    raise CusException.NotValidFileExtension(f"Path's Extension is not Supported: {path}")
        except CusException as exception:
            ErrorLogger.exception(exception)

        # we have array of scannable files, either single or multiple files
        Logger.info(f"Scannable files founded: {scannable_files}")

        Logger.info("Starting file data extraction")
        try:
            for file in scannable_files:
                scanned_files_info.append(get_file_info(file))
        except CusException as exception:
            ErrorLogger.exception(exception)

        Logger.info("Scanning for File Info Completed")
        return scanned_files_info



# traverse the directory recursively. getting every file then checking if the file extension is supported
    def traverse_directory(self, root: Path) -> list:
        Logger.info(f"Starting traversing the directory: {root}")
        files = []
        for file in root.rglob("*"):
            if file.suffix.lower() in self.SUPPORTED_EXTENTIONS:
                files.append(file)
        return files



#================================================
#
#   Utility funtions
#
#================================================

HASH_CHUNK_SIZE = 1024 * 1024 # 1 MB

def get_file_info(path) -> FileInfo:
    Logger.debug(f"Creating file info for Path: {path}")

    stat = path.stat()

    file_info = FileInfo(
         path=str(path.resolve()),
         filename=path.name,
         extension=path.suffix.lower(),
         size_bytes=stat.st_size,
         created_at=_format_timestamp(stat.st_ctime),
         modified_at=_format_timestamp(stat.st_mtime),
         content_hash=_calculate_hash(path)
    )

    Logger.debug(f"FileInfo created for Path: {path}")
    return file_info


def _calculate_hash(path: Path) -> str:
        """
        Calculate the SHA-256 hash of a file.
        """
        import hashlib

        Logger.debug(f"Calculating content hash: {path}")

        sha256 = hashlib.sha256()

        with path.open("rb") as file:
            while chunk := file.read(HASH_CHUNK_SIZE):
                sha256.update(chunk)

        return sha256.hexdigest()

def _format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()