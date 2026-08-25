CREATE TABLE IF NOT EXISTS directories (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    is_active INTEGER NOT NULL,
    registered_at TEXT NOT NULL,
    last_scan_at TEXT
);

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    directory_id INTEGER NOT NULL,
    path TEXT UNIQUE NOT NULL,
    filename TEXT NOT NULL,
    extension TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    modified_at TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    is_deleted INTEGER NOT NULL,
    discovered_at TEXT NOT NULL,
    last_seen_at TEXT,

    FOREIGN KEY (directory_id)
        REFERENCES directories(id)
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    file_id INTEGER UNIQUE NOT NULL,
    document_type TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    processing_status TEXT NOT NULL,
    processing_error TEXT,
    processed_at TEXT NOT NULL,

    FOREIGN KEY (file_id)
        REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    start_offset INTEGER,
    end_offset INTEGER,

    FOREIGN KEY (document_id)
        REFERENCES documents(id),

    UNIQUE (document_id, chunk_index)
);

CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY,
    chunk_id INTEGER NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    dimensions INTEGER NOT NULL,
    vector BLOB NOT NULL,
    created_at TEXT NOT NULL,

    FOREIGN KEY (chunk_id)
        REFERENCES document_chunks(id),

    UNIQUE (chunk_id, model_name, model_version)
);

-- FTS5 virtual table.
-- Will be implemented later by SchemaManager.create_fts()

-- CREATE VIRTUAL TABLE IF NOT EXISTS document_search
-- USING fts5(
--     chunk_id UNINDEXED,
--     content
-- );