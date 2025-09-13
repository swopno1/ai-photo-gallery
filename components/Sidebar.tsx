import Link from 'next/link';

export default function Sidebar() {
  return (
    <div className="w-64 bg-gradient-to-b from-gray-800 to-gray-900 p-5 flex flex-col shadow-lg h-screen">
      <h1 className="text-2xl font-bold mb-10 text-white">Photo Album</h1>
      <nav>
        <ul>
          <li className="mb-4">
            <Link href="/photos" className="flex items-center p-3 text-gray-300 hover:bg-blue-500 hover:text-white rounded-lg transition-all duration-300 ease-in-out transform hover:scale-105">
              <span className="mr-4 text-2xl">🖼️</span>
              <span className="font-medium">Albums</span>
            </Link>
          </li>
          <li className="mb-4">
            <Link href="/faces" className="flex items-center p-3 text-gray-300 hover:bg-purple-500 hover:text-white rounded-lg transition-all duration-300 ease-in-out transform hover:scale-105">
              <span className="mr-4 text-2xl">👥</span>
              <span className="font-medium">Faces</span>
            </Link>
          </li>
          <li className="mb-4">
            <Link href="/tags" className="flex items-center p-3 text-gray-300 hover:bg-green-500 hover:text-white rounded-lg transition-all duration-300 ease-in-out transform hover:scale-105">
              <span className="mr-4 text-2xl">🏷️</span>
              <span className="font-medium">Tags</span>
            </Link>
          </li>
          <li className="mb-4">
            <Link href="/setting" className="flex items-center p-3 text-gray-300 hover:bg-yellow-500 hover:text-white rounded-lg transition-all duration-300 ease-in-out transform hover:scale-105">
              <span className="mr-4 text-2xl">⚙️</span>
              <span className="font-medium">Settings</span>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
