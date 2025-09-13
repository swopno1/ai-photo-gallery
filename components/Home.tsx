"use client";

import React, { useState } from "react";

const Home = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch("http://localhost:8000/run-pipeline/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}), // Use settings.json on backend
      });
      const data = await res.json();
      if (data.status === "started") {
        setStatus("Processing started!");
      } else {
        setStatus(data.message || "Failed to start processing.");
      }
    } catch (e) {
      setStatus("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-12 bg-gray-900">
      <div className="text-center">
        <h2 className="text-5xl font-extrabold text-white mb-4 leading-tight">
          Welcome to Your Digital Photo Haven
        </h2>
        <p className="text-xl text-gray-400 mb-8">
          Organize, view, and cherish your memories like never before.
        </p>
        <div className="mt-8">
          <p className="text-lg text-gray-500 mb-8">
            Get started by selecting a category from the sidebar.
          </p>
          <button
            onClick={handleProcess}
            className="px-6 py-3 rounded bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Processing..." : "Start Processing Images"}
          </button>
          {status && (
            <div className="mt-4 text-lg text-green-400">{status}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
