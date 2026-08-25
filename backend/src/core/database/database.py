from datetime import datetime
from pathlib import Path

from src.logging.logger import Logger, ErrorLogger
from src.core.database.ConnectionManager import ConnectionManager
from src.core.database.SchemaManager import SchemaManager


class Database:

    def __init__(self, database_path: str):
        self.connection_manager = ConnectionManager(database_path) # type: ignore

        self.schema_manager = SchemaManager(
            self.connection_manager
        )

    # ============================================================
    # Database lifecycle
    # ============================================================

    def initialize(self) -> None:
        Logger.info("Initializing database")

        try:
            self.connection_manager.connect()
            self.schema_manager.create_schema()

            Logger.info("Database initialized successfully")

        except Exception as exception:
            ErrorLogger.exception(exception)

            self.connection_manager.close()

            raise

    def close(self) -> None:
        Logger.info("Closing database")

        try:
            self.connection_manager.close()

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    # ============================================================
    # Transaction management
    # ============================================================

    def begin_transaction(self) -> None:
        self.connection_manager.begin_transaction()

    def commit(self) -> None:
        self.connection_manager.commit()

    def rollback(self) -> None:
        self.connection_manager.rollback()

    # ============================================================
    # Directory operations
    # ============================================================

    def add_directory(
        self,
        path: str,
        name: str,
        is_active: int = 1
    ) -> int | None:
        Logger.debug(f"Adding directory to database: {path}")

        connection = self._get_connection()

        registered_at = self._current_timestamp()

        try:
            cursor = connection.execute(
                """
                INSERT INTO directories (
                    path,
                    name,
                    is_active,
                    registered_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    path,
                    name,
                    is_active,
                    registered_at
                )
            )

            Logger.debug(
                f"Directory added successfully: {path}"
            )

            return cursor.lastrowid

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def get_directory(self, path: str):
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    path,
                    name,
                    is_active,
                    registered_at,
                    last_scan_at
                FROM directories
                WHERE path = ?
                """,
                (path,)
            )

            return cursor.fetchone()

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def update_directory_scan_time(self, directory_id: int) -> None:
        connection = self._get_connection()

        try:
            connection.execute(
                """
                UPDATE directories
                SET last_scan_at = ?
                WHERE id = ?
                """,
                (
                    self._current_timestamp(),
                    directory_id
                )
            )

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def delete_directory(self, directory_id: int) -> None:
        connection = self._get_connection()

        try:
            connection.execute(
                """
                DELETE FROM directories
                WHERE id = ?
                """,
                (directory_id,)
            )

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    # ============================================================
    # File operations
    # ============================================================

    def add_file(
        self,
        directory_id: int,
        path: str,
        filename: str,
        extension: str,
        size_bytes: int,
        created_at: str,
        modified_at: str,
        content_hash: str,
        is_deleted: int = 0
    ) -> int | None:
        Logger.debug(f"Adding file to database: {path}")

        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO files (
                    directory_id,
                    path,
                    filename,
                    extension,
                    size_bytes,
                    created_at,
                    modified_at,
                    content_hash,
                    is_deleted,
                    discovered_at,
                    last_seen_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    directory_id,
                    path,
                    filename,
                    extension,
                    size_bytes,
                    created_at,
                    modified_at,
                    content_hash,
                    is_deleted,
                    self._current_timestamp(),
                    self._current_timestamp()
                )
            )

            Logger.debug(
                f"File added successfully: {path}"
            )

            return cursor.lastrowid

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def get_file(self, path: str):
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    directory_id,
                    path,
                    filename,
                    extension,
                    size_bytes,
                    created_at,
                    modified_at,
                    content_hash,
                    is_deleted,
                    discovered_at,
                    last_seen_at
                FROM files
                WHERE path = ?
                """,
                (path,)
            )

            return cursor.fetchone()

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def update_file(
        self,
        file_id: int,
        size_bytes: int,
        modified_at: str,
        content_hash: str
    ) -> None:
        connection = self._get_connection()

        try:
            connection.execute(
                """
                UPDATE files
                SET
                    size_bytes = ?,
                    modified_at = ?,
                    content_hash = ?,
                    is_deleted = 0,
                    last_seen_at = ?
                WHERE id = ?
                """,
                (
                    size_bytes,
                    modified_at,
                    content_hash,
                    self._current_timestamp(),
                    file_id
                )
            )

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def mark_file_deleted(self, file_id: int) -> None:
        connection = self._get_connection()

        try:
            connection.execute(
                """
                UPDATE files
                SET
                    is_deleted = 1,
                    last_seen_at = ?
                WHERE id = ?
                """,
                (
                    self._current_timestamp(),
                    file_id
                )
            )

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def update_file_last_seen(self, file_id: int) -> None:
        connection = self._get_connection()

        try:
            connection.execute(
                """
                UPDATE files
                SET
                    last_seen_at = ?,
                    is_deleted = 0
                WHERE id = ?
                """,
                (
                    self._current_timestamp(),
                    file_id
                )
            )

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    # ============================================================
    # Document operations
    # ============================================================

    def add_document(
        self,
        file_id: int,
        document_type: str,
        extracted_text: str,
        processing_status: str,
        processing_error: str | None = None
    ) -> int | None:
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO documents (
                    file_id,
                    document_type,
                    extracted_text,
                    processing_status,
                    processing_error,
                    processed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    file_id,
                    document_type,
                    extracted_text,
                    processing_status,
                    processing_error,
                    self._current_timestamp()
                )
            )

            return cursor.lastrowid

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def get_document(self, file_id: int):
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    file_id,
                    document_type,
                    extracted_text,
                    processing_status,
                    processing_error,
                    processed_at
                FROM documents
                WHERE file_id = ?
                """,
                (file_id,)
            )

            return cursor.fetchone()

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def update_document_status(
        self,
        document_id: int,
        processing_status: str,
        processing_error: str | None = None
    ) -> None:
        connection = self._get_connection()

        try:
            connection.execute(
                """
                UPDATE documents
                SET
                    processing_status = ?,
                    processing_error = ?,
                    processed_at = ?
                WHERE id = ?
                """,
                (
                    processing_status,
                    processing_error,
                    self._current_timestamp(),
                    document_id
                )
            )

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    # ============================================================
    # Chunk operations
    # ============================================================

    def add_chunk(
        self,
        document_id: int,
        chunk_index: int,
        content: str,
        start_offset: int | None = None,
        end_offset: int | None = None
    ) -> int | None:
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO document_chunks (
                    document_id,
                    chunk_index,
                    content,
                    start_offset,
                    end_offset
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    chunk_index,
                    content,
                    start_offset,
                    end_offset
                )
            )

            return cursor.lastrowid

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def get_document_chunks(self, document_id: int):
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    document_id,
                    chunk_index,
                    content,
                    start_offset,
                    end_offset
                FROM document_chunks
                WHERE document_id = ?
                ORDER BY chunk_index
                """,
                (document_id,)
            )

            return cursor.fetchall()

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    # ============================================================
    # Embedding operations
    # ============================================================

    def add_embedding(
        self,
        chunk_id: int,
        model_name: str,
        model_version: str,
        dimensions: int,
        vector: bytes
    ) -> int | None:
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO embeddings (
                    chunk_id,
                    model_name,
                    model_version,
                    dimensions,
                    vector,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    chunk_id,
                    model_name,
                    model_version,
                    dimensions,
                    vector,
                    self._current_timestamp()
                )
            )

            return cursor.lastrowid

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    def get_embedding(
        self,
        chunk_id: int,
        model_name: str,
        model_version: str
    ):
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    chunk_id,
                    model_name,
                    model_version,
                    dimensions,
                    vector,
                    created_at
                FROM embeddings
                WHERE
                    chunk_id = ?
                    AND model_name = ?
                    AND model_version = ?
                """,
                (
                    chunk_id,
                    model_name,
                    model_version
                )
            )

            return cursor.fetchone()

        except Exception as exception:
            ErrorLogger.exception(exception)
            raise

    # ============================================================
    # Utility methods
    # ============================================================

    def _get_connection(self):
        if self.connection_manager.connection is None:
            raise RuntimeError(
                "Database is not connected"
            )

        return self.connection_manager.connection

    @staticmethod
    def _current_timestamp() -> str:
        return datetime.now().isoformat()