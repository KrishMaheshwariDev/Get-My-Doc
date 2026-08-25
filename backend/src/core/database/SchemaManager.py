from pathlib import Path

from src.logging.logger import Logger, ErrorLogger
from src.core.database.ConnectionManager import ConnectionManager


class SchemaManager:

    def __init__(
        self,
        connection_manager: ConnectionManager,
        schema_path: str | None = None
    ):
        self.connection_manager = connection_manager

        if schema_path is None:
            self.schema_path = Path(__file__).resolve().parent / "schema.sql"
        else:
            self.schema_path = Path(schema_path)
    
    def create_schema(self) -> None:
        Logger.info(
            f"Creating database schema from: {self.schema_path}"
        )

        if self.connection_manager.connection is None:
            raise RuntimeError(
                "Cannot create schema: database is not connected"
            )

        try:
            if not self.schema_path.exists():
                raise FileNotFoundError(
                    f"Schema file not found: {self.schema_path}"
                )

            with self.schema_path.open(
                "r",
                encoding="utf-8"
            ) as schema_file:
                schema = schema_file.read()

            self.connection_manager.connection.executescript(schema)

            Logger.info("Database schema created successfully")

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def create_indexes(self) -> None:
        pass

    def create_fts(self) -> None:
        pass

    def migrate(self) -> None:
        pass