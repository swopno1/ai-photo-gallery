"use client";
import { useParams } from "next/navigation";

const facePhotos = [
  "/placeholder.jpg",
  "/placeholder.jpg",
  "/placeholder.jpg",
];

export default function FaceAlbumPage() {
  const { person_id } = useParams();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Photos of Person {person_id}</h1>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {facePhotos.map((src, idx) => (
          <img
            key={idx}
            src={src}
            alt={`Face ${idx}`}
            className="h-48 w-full object-cover rounded-xl shadow"
          />
        ))}
      </div>
    </div>
  );
}
