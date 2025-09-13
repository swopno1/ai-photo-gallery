import React from 'react';
import Link from 'next/link';

const Home = () => {
  return (
    <div className="flex h-screen bg-gray-900 text-white font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-gradient-to-b from-gray-800 to-gray-900 p-5 flex flex-col shadow-lg">
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
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-12 bg-gray-900">
        <div className="text-center">
            <h2 className="text-5xl font-extrabold text-white mb-4 leading-tight">
                Welcome to Your Digital Photo Haven
            </h2>
            <p className="text-xl text-gray-400 mb-8">
                Organize, view, and cherish your memories like never before.
            </p>
            <div className="mt-8">
                <p className="text-lg text-gray-500">
                    Get started by selecting a category from the sidebar.
                </p>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
