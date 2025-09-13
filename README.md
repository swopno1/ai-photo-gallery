

# 📸 AI Photo Gallery

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

AI-powered **photo management tool** that organizes your photos by **date, event, and faces**.
It detects duplicates, extracts EXIF metadata (date, GPS), clusters faces, and provides a **modern Next.js gallery UI** for browsing — all **offline** and privacy-friendly.

---

## ✨ Features

- 🗓 **Event-based organization** → Groups photos by date + GPS location  
- 😀 **Face recognition & clustering** → Search all photos with the same person using the `face_recognition` library.
- 📂 **Smart file organization** → Automatically sorts into folders, moves duplicates aside  
- 🎨 **Beautiful UI** → Built with Next.js 15 + TailwindCSS, filterable gallery view  
- ⚡ **Fast & local** → Runs offline with a Python pipeline.
- 🔒 **Privacy-first** → Your photos and faces never leave your machine  

---

## 📂 Project Structure

```bash
project-root/
│
├─ app/                       # Next.js App Router
│   ├─ layout.tsx             # Root layout
│   ├─ page.tsx               # Home page (optional: overview)
│   ├─ photos/                # Photos section
│   │   ├─ [album]/           # Dynamic route for Event Albums
│   │   │   └─ page.tsx       # Album gallery page
│   │   └─ page.tsx           # All albums overview
│   ├─ faces/                 # Face Albums (optional, future)
│   │   └─ [person_id]/page.tsx
│   └─ tags/                  # Tags view (optional, future)
│       └─ [tag]/page.tsx
│
├─ components/                # React Components
│   ├─ PhotoCard.tsx           # Single photo card component
│   └─ GalleryGrid.tsx         # Optional: reusable grid component
│
├─ lib/
│   └─ db.ts                   # SQLite access helper functions
│
├─ python_pipeline/           # Python AI backend
│   ├─ process_photos.py       # Core AI pipeline script
│   ├─ face_embeddings.db      # Optional: serialized face DB
│   └─ requirements.txt        # Python dependencies
│
├─ photos_folder/             # Original photos to process
│
├─ duplicates/                # Duplicates detected by pipeline
│
├─ public/                    # Public folder for Next.js static files
│
├─ tailwind.config.js
├─ tsconfig.json
├─ package.json
└─ next.config.js
```
  

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed on your system:

-   **Python 3.8+**
-   **Node.js 18.0+**
-   **npm**

### 1. Fork and Clone the Repository

First, fork the repository to your own GitHub account. Then, clone your forked repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/ai-photo-gallery.git
cd ai-photo-gallery
```

### 2. Set Up the Python Environment

Navigate to the `python_pipeline` directory and create a virtual environment:

```bash
cd python_pipeline
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Process Your Photos

Place your photos in the `photos_folder` directory. Then, run the processing script:

```bash
python process_photos.py --input ../photos_folder
```

This will organize your photos, detect faces, and create a `photos.db` file in the `python_pipeline` directory.

### 4. Set Up and Run the Frontend

Navigate back to the root directory and install the npm packages:

```bash
cd ..
npm install
```

Run the Next.js development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the photo gallery.

---

## 🤖 Offline AI and Privacy

This project is designed to be **100% offline**. All AI processing, including face detection and clustering, happens locally on your machine.

-   **No data is sent to the cloud.**
-   **No external AI services are used.**
-   **Your photos and personal data remain private.**

The face recognition feature is powered by the `face_recognition` library, which uses a pre-trained model to find faces in your photos.

---

## 🛠 How It Works

The core of this project is the Python script `python_pipeline/process_photos.py`. When you run this script, it performs the following steps:

1.  **Initializes a SQLite Database**: Creates a `photos.db` file to store all the metadata about your photos.
2.  **Scans the Input Folder**: Recursively scans the folder you provide as input.
3.  **Detects Duplicates**: Calculates a hash for each photo to identify and move exact duplicates to the `duplicates` folder.
4.  **Extracts EXIF Metadata**: Reads the EXIF data from each photo to get the date taken and GPS coordinates.
5.  **Organizes Photos**: Creates folders based on the year and month the photos were taken and moves the photos into them.
6.  **Detects Faces**: Uses the `face_recognition` library to find all faces in each photo.
7.  **Saves Metadata**: Saves all the extracted information (file path, date, event, faces, etc.) into the SQLite database.

The Next.js frontend then reads the `photos.db` database to display the photo gallery.
