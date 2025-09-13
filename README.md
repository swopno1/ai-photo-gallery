This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Project Structure

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
