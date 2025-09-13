import shutil
def generate_smart_tags(top_k=3):
    """
    Generate smart tags for each photo using a lightweight local model (MobileNetV2).
    Only run when explicitly called.
    """
    import torch
    from torchvision import models, transforms
    from PIL import Image
    import json
    import urllib.request

    # Load model and labels
    model = models.mobilenet_v2(pretrained=True)
    model.eval()
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Download ImageNet labels if not present
    LABELS_PATH = "imagenet_class_index.json"
    try:
        with open(LABELS_PATH, "r") as f:
            class_idx = json.load(f)
    except FileNotFoundError:
        url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        urllib.request.urlretrieve(url, LABELS_PATH)
        with open(LABELS_PATH, "r") as f:
            class_idx = {str(i): [str(i), line.strip()] for i, line in enumerate(f.readlines())}

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, path FROM photos")
    rows = c.fetchall()
    for pid, img_path in rows:
        try:
            input_image = Image.open(img_path).convert("RGB")
            input_tensor = preprocess(input_image)
            input_batch = input_tensor.unsqueeze(0)
            with torch.no_grad():
                output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            topk = torch.topk(probabilities, top_k)
            tags = [class_idx[str(idx.item())][1] for idx in topk.indices]
            tags_str = ",".join(tags)
            c.execute("UPDATE photos SET tags=? WHERE id=?", (tags_str, pid))
            print(f"[TAGS] {img_path}: {tags_str}")
        except Exception as e:
            print(f"[WARN] Tagging failed for {img_path}: {e}")
    conn.commit()
    conn.close()
    print("Smart tag generation complete.")
def cluster_faces_by_embedding(eps=0.6, min_samples=2):
    """
    Cluster face embeddings using DBSCAN and update face_cluster in DB.
    eps: DBSCAN distance threshold (tune as needed)
    min_samples: minimum faces per cluster
    """
    import numpy as np
    from sklearn.cluster import DBSCAN
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, photo_id, embedding FROM faces")
    rows = c.fetchall()
    if not rows:
        print("No face embeddings found for clustering.")
        conn.close()
        return

    ids = []
    photo_ids = []
    embeddings = []
    for row in rows:
        fid, pid, emb_blob = row
        try:
            emb = np.frombuffer(emb_blob, dtype=np.float64)
            if emb.size == 0:
                continue
            ids.append(fid)
            photo_ids.append(pid)
            embeddings.append(emb)
        except Exception:
            continue

    if not embeddings:
        print("No valid face embeddings for clustering.")
        conn.close()
        return

    X = np.vstack(embeddings)
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(X)
    labels = db.labels_

    # Update faces table with cluster label
    for fid, label in zip(ids, labels):
        cluster_id = f"face_{label}" if label != -1 else None
        c.execute("UPDATE faces SET person_name=? WHERE id=?", (cluster_id, fid))

    # Optionally, update photos table with main face_cluster (first face found per photo)
    for pid in set(photo_ids):
        clusters = [f"face_{labels[i]}" for i, p in enumerate(photo_ids) if p == pid and labels[i] != -1]
        main_cluster = clusters[0] if clusters else None
        c.execute("UPDATE photos SET face_cluster=? WHERE id=?", (main_cluster, pid))

    conn.commit()
    conn.close()
    print(f"Clustered {len(ids)} faces into {len(set(labels)) - (1 if -1 in labels else 0)} groups.")
from sklearn.cluster import DBSCAN
import numpy as np
def cluster_photos_by_event(eps_time=3*3600, eps_distance=0.01, min_samples=2):
    """
    Cluster photos by time (seconds) and location (GPS degrees).
    eps_time: max time difference in seconds for clustering (default 3 hours)
    eps_distance: max GPS distance in degrees (default ~1km)
    min_samples: minimum photos per event
    """
    rows = fetch_photo_metadata()
    if not rows:
        print("No photos with date and GPS metadata found.")
        return

    # Prepare feature vectors: [timestamp, lat, lon]
    features = []
    id_list = []
    for row in rows:
        pid, date_taken, lat, lon = row
        try:
            dt = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
            timestamp = dt.timestamp()
            features.append([timestamp, float(lat), float(lon)])
            id_list.append(pid)
        except Exception as e:
            continue

    if not features:
        print("No valid features for clustering.")
        return

    X = np.array(features)
    # Normalize time and location for DBSCAN
    X_norm = X.copy()
    X_norm[:,0] = X[:,0] / eps_time
    X_norm[:,1] = X[:,1] / eps_distance
    X_norm[:,2] = X[:,2] / eps_distance

    db = DBSCAN(eps=1.0, min_samples=min_samples).fit(X_norm)
    labels = db.labels_

    # Update DB with event labels
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for pid, label in zip(id_list, labels):
        event_label = f"event_{label}" if label != -1 else None
        c.execute("UPDATE photos SET event=? WHERE id=?", (event_label, pid))
    conn.commit()
    conn.close()
    print(f"Clustered {len(id_list)} photos into {len(set(labels))- (1 if -1 in labels else 0)} events.")
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


def fetch_photo_metadata():
    """Fetch all photos' id, date_taken, gps_lat, gps_lon from the database for clustering."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, date_taken, gps_lat, gps_lon FROM photos WHERE date_taken IS NOT NULL AND gps_lat IS NOT NULL AND gps_lon IS NOT NULL")
    rows = c.fetchall()
    conn.close()
    return rows


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
    camera_make, camera_model, lens_model = None, None, None
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

        if "Image Make" in tags:
            camera_make = str(tags["Image Make"])
        if "Image Model" in tags:
            camera_model = str(tags["Image Model"])
        if "EXIF LensModel" in tags:
            lens_model = str(tags["EXIF LensModel"])

    except Exception as e:
        print(f"[WARN] Could not read EXIF for {img_path}: {e}")

    return taken_date, gps_lat, gps_lon, camera_make, camera_model, lens_model


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


def save_photo_metadata(file_path, filename, file_hash, phash, date_taken, gps_lat, gps_lon, camera_make, camera_model, lens_model, event=None, tags=None, duplicate_group=None):
    """Save photo metadata into SQLite DB, including camera info and duplicate group."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO photos 
        (path, filename, file_hash, phash, date_taken, gps_lat, gps_lon, camera_make, camera_model, lens_model, event, tags, duplicate_group) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (file_path, filename, file_hash, phash, date_taken, gps_lat, gps_lon, camera_make, camera_model, lens_model, event, tags, duplicate_group))
    conn.commit()
    conn.close()


def process_folder(input_folder, output_base="./organized_photos", duplicate_folder="./duplicates"):
    """Process all photos in a folder, sort, and move."""
    init_db()
    seen_hashes = set()
    seen_phashes = {}
    duplicate_group_counter = 1


    for root, _, files in os.walk(input_folder):
        for file in files:
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            file_path = os.path.join(root, file)
            file_hash = compute_file_hash(file_path)
            phash = compute_phash(file_path)

            # Duplicate check

            # Exact duplicate check
            if file_hash in seen_hashes:
                os.makedirs(duplicate_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(duplicate_folder, file))
                print(f"[DUPLICATE] {file} moved to duplicates (exact hash)")
                continue
            seen_hashes.add(file_hash)

            # Near-duplicate check using pHash
            duplicate_group = None
            if phash:
                for prev_phash, group_id in seen_phashes.items():
                    try:
                        dist = imagehash.hex_to_hash(phash) - imagehash.hex_to_hash(prev_phash)
                        if dist <= 5:  # threshold for near-duplicate (tune as needed)
                            os.makedirs(duplicate_folder, exist_ok=True)
                            shutil.move(file_path, os.path.join(duplicate_folder, file))
                            print(f"[NEAR-DUPLICATE] {file} moved to duplicates (pHash dist={dist})")
                            duplicate_group = group_id
                            break
                    except Exception:
                        continue
                if duplicate_group is None:
                    # New unique pHash, assign new group
                    duplicate_group = f"group_{duplicate_group_counter}"
                    seen_phashes[phash] = duplicate_group
                    duplicate_group_counter += 1
            else:
                duplicate_group = None


            # Metadata
            taken_date, gps_lat, gps_lon, camera_make, camera_model, lens_model = get_exif_metadata(file_path)

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
            shutil.move(file_path, new_path)

            # Save metadata, including duplicate_group
            save_photo_metadata(new_path, file, file_hash, phash, taken_date, gps_lat, gps_lon, camera_make, camera_model, lens_model, event=folder_name, tags=None, duplicate_group=duplicate_group)

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

    # After processing all photos, cluster by event and faces
    cluster_photos_by_event()
    cluster_faces_by_embedding()


if __name__ == "__main__":
    import argparse

    import os
    parser = argparse.ArgumentParser(description="AI Image Organizer")
    parser.add_argument("--input", help="Path to input folder of photos")
    parser.add_argument("--output", help="Path to output/organized folder")
    parser.add_argument("--duplicates", help="Path to duplicates folder")
    parser.add_argument("--generate-tags", action="store_true", help="Generate smart tags for all photos (optional, slow)")
    args = parser.parse_args()


    # Use CLI args, else env vars, else settings.json, else defaults
    def load_settings():
        import json, os
        SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r") as f:
                return json.load(f)
        return {}

    settings = load_settings()
    input_folder = args.input or os.environ.get("PHOTO_INPUT_FOLDER") or settings.get("input")
    output_folder = args.output or os.environ.get("PHOTO_OUTPUT_FOLDER") or settings.get("output") or "./organized_photos"
    duplicates_folder = args.duplicates or os.environ.get("PHOTO_DUPLICATE_FOLDER") or settings.get("duplicates") or "./duplicates"

    if input_folder:
        process_folder(input_folder, output_base=output_folder, duplicate_folder=duplicates_folder)
    if args.generate_tags:
        generate_smart_tags()
