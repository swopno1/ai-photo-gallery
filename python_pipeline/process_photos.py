import os
import cv2
import face_recognition
import hashlib
import sqlite3
import imagehash
from PIL import Image
from datetime import datetime
import exifread

# Database path
DB_PATH = "photos.db"


def init_db():
    """Initialize SQLite DB with schema."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Photos table
    c.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            filename TEXT,
            date_taken TEXT,
            event TEXT,
            tags TEXT,
            face_cluster TEXT,
            duplicate_group TEXT,
            file_hash TEXT,
            phash TEXT,
            gps_lat REAL,
            gps_lon REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Faces table
    c.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_id INTEGER,
            person_name TEXT,
            embedding BLOB,
            FOREIGN KEY(photo_id) REFERENCES photos(id)
        )
    """)

    conn.commit()
    conn.close()


def get_exif_metadata(img_path):
    """Extract EXIF metadata like date and GPS from an image."""
    taken_date, gps_lat, gps_lon = None, None, None
    try:
        with open(img_path, "rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF")

        if "EXIF DateTimeOriginal" in tags:
            taken_date = str(tags["EXIF DateTimeOriginal"])

        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat_values = tags["GPS GPSLatitude"].values
            lon_values = tags["GPS GPSLongitude"].values

            def convert_to_degrees(value):
                d, m, s = [x.num / x.den for x in value]
                return d + (m / 60.0) + (s / 3600.0)

            gps_lat = convert_to_degrees(lat_values)
            gps_lon = convert_to_degrees(lon_values)

    except Exception as e:
        print(f"[WARN] Could not read EXIF for {img_path}: {e}")

    return taken_date, gps_lat, gps_lon


def compute_file_hash(img_path):
    """Compute hash of file contents to detect exact duplicates."""
    hash_md5 = hashlib.md5()
    with open(img_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compute_phash(img_path):
    """Compute perceptual hash for near-duplicate detection."""
    try:
        with Image.open(img_path) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        print(f"[WARN] Could not compute pHash for {img_path}: {e}")
        return None


def detect_faces(img_path):
    """Extract face embeddings from an image."""
    try:
        image = face_recognition.load_image_file(img_path)
        return face_recognition.face_encodings(image)
    except Exception as e:
        print(f"[WARN] Could not detect faces in {img_path}: {e}")
        return []


def save_photo_metadata(file_path, filename, file_hash, phash, date_taken, gps_lat, gps_lon, event=None, tags=None):
    """Save photo metadata into SQLite DB."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO photos 
        (path, filename, file_hash, phash, date_taken, gps_lat, gps_lon, event, tags) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (file_path, filename, file_hash, phash, date_taken, gps_lat, gps_lon, event, tags))
    conn.commit()
    conn.close()


def process_folder(input_folder, output_base="./organized_photos", duplicate_folder="./duplicates"):
    """Process all photos in a folder, sort, and move."""
    init_db()
    seen_hashes = set()

    for root, _, files in os.walk(input_folder):
        for file in files:
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            file_path = os.path.join(root, file)
            file_hash = compute_file_hash(file_path)
            phash = compute_phash(file_path)

            # Duplicate check
            if file_hash in seen_hashes:
                os.makedirs(duplicate_folder, exist_ok=True)
                os.rename(file_path, os.path.join(duplicate_folder, file))
                print(f"[DUPLICATE] {file} moved to duplicates")
                continue
            seen_hashes.add(file_hash)

            # Metadata
            taken_date, gps_lat, gps_lon = get_exif_metadata(file_path)

            # Event folder (YYYY-MM)
            folder_name = "Unknown_Date"
            if taken_date:
                try:
                    dt = datetime.strptime(taken_date, "%Y:%m:%d %H:%M:%S")
                    folder_name = f"{dt.year}-{dt.month:02d}"
                except Exception:
                    pass

            target_folder = os.path.join(output_base, folder_name)
            os.makedirs(target_folder, exist_ok=True)
            new_path = os.path.join(target_folder, file)
            os.rename(file_path, new_path)

            # Save metadata
            save_photo_metadata(new_path, file, file_hash, phash, taken_date, gps_lat, gps_lon, event=folder_name)

            # Face detection + save
            embeddings = detect_faces(new_path)
            if embeddings:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                for emb in embeddings:
                    c.execute("INSERT INTO faces (photo_id, person_name, embedding) VALUES ((SELECT id FROM photos WHERE path=?), ?, ?)",
                              (new_path, "Unknown", emb.tobytes()))
                conn.commit()
                conn.close()

            print(f"[OK] {file} → {new_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Image Organizer")
    parser.add_argument("--input", required=True, help="Path to input folder of photos")
    args = parser.parse_args()

    process_folder(args.input)
