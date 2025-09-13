"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type Photo = {
  id: number;
  path: string;
  date_taken: string;
};

export default function AlbumPage() {
  const { album } = useParams();
  const [photos, setPhotos] = useState<Photo[]>([]);

  useEffect(() => {
    fetch(`/api/albums/${album}`)
      .then((res) => res.json())
      .then((data) => setPhotos(data));
  }, [album]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Album: {album}</h1>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {photos.map((photo) => (
          <img
            key={photo.id}
            src={photo.path}
            alt={`Photo ${photo.id}`}
            className="h-48 w-full object-cover rounded-xl shadow"
          />
        ))}
      </div>
    </div>
  );
}
