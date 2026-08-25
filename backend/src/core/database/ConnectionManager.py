import sqlite3
from pathlib import Path

from src.logging.logger import Logger, ErrorLogger

class ConnectionManager:

    def __int__(self, database_path: str):
        self.database_path = Path(database_path)
        self.connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        Logger.info(f"Connecting to SQLite Database: {self.database_path}")

        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)

            self.connection = sqlite3.connect(self.database_path)

            self.connection.execute("PRAGMA foreign_keys = ON")

            Logger.info(f"SQLite Database connection establised")
        except Exception as e:
            ErrorLogger.exception(e)
            raise

    def close(self) -> None:
        if self.connection is None:
            return

        Logger.info("Closing the SQLite database connection")

        try:
            self.connection.close()
            self.connection = None

            Logger.info("SQLite database connection is closed")
        except Exception as e:
            ErrorLogger.exception(e)
            raise

    def begin_transaction(self) -> None:
        if self.connection is None:
            raise RuntimeError(
                "Cannot begin transaction: Database is not connected"
            )

        Logger.debug("Beginning database transaction")

        try:
            self.connection.execute("BEGIN")
        except Exception as e:
            ErrorLogger.exception(e)
            raise

    def commit(self) -> None:
        if self.connection is None:
            raise RuntimeError(
                "Cannot commit transaction: Database is not connected"
            )

        Logger.debug("Commiting database transaction")

        try:
            self.connection.commit()
        except Exception as e:
            ErrorLogger.exception(e)
            raise

    def rollback(self) -> None:
        if self.connection is None:
            raise RuntimeError(
                "Connot rollback transaction: Database is not connected"
            )

        Logger.debug("Rollback database transaction")

        try:
            self.connection.rollback()
        except Exception as e:
            ErrorLogger.exception(e)
            raise