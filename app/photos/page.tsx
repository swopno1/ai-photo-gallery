import Link from "next/link";

type Album = {
  name: string;
  count: number;
  cover: string;
};

async function getAlbums(): Promise<Album[]> {
  const res = await fetch("http://localhost:3000/api/albums", { cache: "no-store" });
  return res.json();
}

export default async function PhotosPage() {
  const albums = await getAlbums();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Photo Albums</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {albums.map((album) => (
          <Link key={album.name} href={`/photos/${album.name}`}>
            <div className="group cursor-pointer rounded-2xl overflow-hidden shadow hover:shadow-lg transition">
              <img
                src={album.cover}
                alt={album.name}
                className="h-48 w-full object-cover group-hover:scale-105 transition"
              />
              <div className="p-4 bg-white">
                <h2 className="font-semibold text-lg">{album.name}</h2>
                <p className="text-gray-500">{album.count} photos</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
