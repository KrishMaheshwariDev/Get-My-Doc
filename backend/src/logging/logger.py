from datetime import datetime
from pathlib import Path
import traceback


class Logger:
    _instance = None
    _log_file = None

    def __new__(cls, logs_directory: Path | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize(logs_directory)

        return cls._instance

    @classmethod
    def _initialize(cls, logs_directory: Path | None = None) -> None:
        if logs_directory is None:
            logs_directory = Path(__file__).resolve().parent.parent.parent / "logs"

        logs_directory = Path(logs_directory)
        logs_directory.mkdir(parents=True, exist_ok=True)

        session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        cls._log_file = logs_directory / f"session_{session_id}.log"

        cls._log_file.touch(exist_ok=False)

        cls._write_session_marker("SESSION START")

    @classmethod
    def info(cls, message: str) -> None:
        cls._write("INFO", message)

    @classmethod
    def debug(cls, message: str) -> None:
        cls._write("DEBUG", message)

    @classmethod
    def warning(cls, message: str) -> None:
        cls._write("WARNING", message)

    @classmethod
    def _write(cls, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}\n"

        with cls._log_file.open("a", encoding="utf-8") as file:
            file.write(entry)
            file.flush()

    @classmethod
    def _write_session_marker(cls, marker: str) -> None:
        with cls._log_file.open("a", encoding="utf-8") as file:
            file.write("=" * 60 + "\n")
            file.write(f"{marker}\n")
            file.write("=" * 60 + "\n")
            file.flush()


class ErrorLogger:
    """Handles errors and exceptions using the active logging session."""
    @classmethod
    def error(cls, message: str) -> None:
        Logger._write("ERROR", message)

    @classmethod
    def exception(cls, exception: Exception) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with Logger._log_file.open("a", encoding="utf-8") as file:
            file.write(
                f"[{timestamp}] [EXCEPTION] "
                f"{type(exception).__name__}: {exception}\n"
            )

            file.write("Traceback:\n")

            file.write(
                "".join(
                    traceback.format_exception(
                        type(exception),
                        exception,
                        exception.__traceback__,
                    )
                )
            )

            file.write("\n")
            file.flush()