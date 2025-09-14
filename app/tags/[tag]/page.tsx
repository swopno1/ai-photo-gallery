"use client";
import Image from "next/image";
import { useParams } from "next/navigation";

const taggedPhotos = [
  "/placeholder.jpg",
  "/placeholder.jpg",
  "/placeholder.jpg",
];

export default function TagPage() {
  const { tag } = useParams();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Photos tagged with “{tag}”</h1>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {taggedPhotos.map((src, idx) => (
          <Image
            key={idx}
            src={`/api/image-proxy?path=${encodeURIComponent(src)}`}
            width={500}
            height={500}
            alt={`Tagged ${idx}`}
            className="h-48 w-full object-cover rounded-xl shadow"
          />
        ))}
      </div>
    </div>
  );
}
