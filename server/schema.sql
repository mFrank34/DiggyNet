-- clients table
CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    key TEXT NOT NULL
);

-- server table (single row)
CREATE TABLE IF NOT EXISTS server (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL
);
