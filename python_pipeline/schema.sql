-- Photos table: core metadata
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL UNIQUE,         -- Full file path
    filename TEXT,                     -- Just the filename
    date_taken TEXT,                   -- EXIF or file timestamp (ISO 8601)
    event TEXT,                        -- Event grouping (date + GPS cluster)
    tags TEXT,                         -- Comma-separated tags (e.g., "beach,holiday")
    face_cluster TEXT,                 -- Face cluster ID (optional)
    duplicate_group TEXT,              -- Group ID for duplicates
    file_hash TEXT,                    -- Exact file hash (MD5/SHA1)
    phash TEXT,                        -- Perceptual hash (pHash/dHash/aHash)
    gps_lat REAL,                      -- GPS latitude
    gps_lon REAL,                      -- GPS longitude
    camera_make TEXT,                  -- Camera make (e.g., Canon, Nikon)
    camera_model TEXT,                 -- Camera model (e.g., EOS 80D)
    lens_model TEXT,                   -- Lens model (if available)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Faces table: face embeddings for clustering
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_id INTEGER,                  -- FK to photos
    person_name TEXT,                  -- Optional label
    embedding BLOB,                    -- Face embedding vector
    FOREIGN KEY(photo_id) REFERENCES photos(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_event ON photos(event);
CREATE INDEX IF NOT EXISTS idx_date_taken ON photos(date_taken);
CREATE INDEX IF NOT EXISTS idx_face_cluster ON photos(face_cluster);
CREATE INDEX IF NOT EXISTS idx_duplicate_group ON photos(duplicate_group);
CREATE INDEX IF NOT EXISTS idx_tags ON photos(tags);
