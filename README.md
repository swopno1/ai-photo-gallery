

# 📸 AI Photo Gallery

AI-powered **photo management tool** that organizes your photos by **date, event, faces, and tags**.  
It detects duplicates, extracts EXIF metadata (date, GPS), clusters faces, and provides a **modern Next.js gallery UI** for browsing — all **offline** and privacy-friendly.

---

## ✨ Features

- 🗓 **Event-based organization** → Groups photos by date + GPS location  
- 😀 **Face recognition & clustering** → Search all photos with the same person  
- 🏷 **AI-powered tagging** → Auto-label photos (e.g., `birthday`, `beach`, `family`)  
- 📂 **Smart file organization** → Automatically sorts into folders, moves duplicates aside  
- 🎨 **Beautiful UI** → Built with Next.js 15 + TailwindCSS, filterable gallery view  
- ⚡ **Fast & local** → Runs offline with [llama.cpp](https://github.com/ggerganov/llama.cpp) and Python pipeline  
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
├─ models/                    # Offline AI models
│   └─ phi-3-mini-instruct-Q4_K_M.gguf
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

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-photo-gallery.git
cd ai-photo-gallery
```

### 2. Python AI Backend (Image Processing)
```bash
cd python_pipeline
pip install -r requirements.txt
python process_photos.py --input /path/to/your/photos
```

### 3. Next.js Frontend (Gallery UI)
```bash
cd nextjs_app
npm install
npm run dev
```
