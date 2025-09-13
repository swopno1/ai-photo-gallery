'use client'

import { useState, useEffect, useRef } from "react";

export default function SettingPage() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [duplicates, setDuplicates] = useState("");
  const [message, setMessage] = useState("");

  const inputRef = useRef<HTMLInputElement>(null);
  const outputRef = useRef<HTMLInputElement>(null);
  const duplicatesRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch("/api/settings")
      .then((res) => res.json())
      .then((data) => {
        setInput(data.input || "");
        setOutput(data.output || "");
        setDuplicates(data.duplicates || "");
      });
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input, output, duplicates }),
    });
    if (res.ok) setMessage("Settings saved!");
    else setMessage("Failed to save settings.");
  };

  return (
    <div className="p-8 max-w-xl mx-auto bg-gray-800 rounded-xl shadow-lg mt-10">
      <h1 className="text-3xl font-bold mb-8 text-yellow-300">Folder Settings</h1>
      <form onSubmit={handleSave} className="space-y-6">
        <div>
          <label className="block font-semibold mb-2 text-gray-200">Input Folder</label>
          <div className="flex gap-2">
            <input type="text" value={input} onChange={e => setInput(e.target.value)} className="w-full border border-gray-600 bg-gray-900 text-gray-100 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-yellow-400" placeholder="/full/path/to/input" />
            <button
              type="button"
              className="bg-yellow-400 text-gray-900 px-3 py-2 rounded cursor-pointer font-semibold hover:bg-yellow-300"
              onClick={() => inputRef.current?.click()}
            >Browse</button>
            <input
              type="file"
              style={{ display: "none" }}
              ref={inputRef}
              //@ts-ignore
              webkitdirectory="true"
              directory="true"
              onChange={e => {
                const files = e.target.files;
                if (files && files.length > 0) {
                  // Get the full path up to the folder
                  const relPath = files[0].webkitRelativePath;
                  const folderPath = relPath.substring(0, relPath.indexOf("/"));
                  // Try to get absolute path if available (not always possible in browser)
                  setInput(folderPath);
                }
              }}
            />
          </div>
        </div>
        <div>
          <label className="block font-semibold mb-2 text-gray-200">Output Folder</label>
          <div className="flex gap-2">
            <input type="text" value={output} onChange={e => setOutput(e.target.value)} className="w-full border border-gray-600 bg-gray-900 text-gray-100 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-yellow-400" placeholder="/full/path/to/output" />
            <button
              type="button"
              className="bg-yellow-400 text-gray-900 px-3 py-2 rounded cursor-pointer font-semibold hover:bg-yellow-300"
              onClick={() => outputRef.current?.click()}
            >Browse</button>
            <input
              type="file"
              style={{ display: "none" }}
              ref={outputRef}
              //@ts-ignore
              webkitdirectory="true"
              directory="true"
              onChange={e => {
                const files = e.target.files;
                if (files && files.length > 0) {
                  const relPath = files[0].webkitRelativePath;
                  const folderPath = relPath.substring(0, relPath.indexOf("/"));
                  setOutput(folderPath);
                }
              }}
            />
          </div>
        </div>
        <div>
          <label className="block font-semibold mb-2 text-gray-200">Duplicates Folder</label>
          <div className="flex gap-2">
            <input type="text" value={duplicates} onChange={e => setDuplicates(e.target.value)} className="w-full border border-gray-600 bg-gray-900 text-gray-100 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-yellow-400" placeholder="/full/path/to/duplicates" />
            <button
              type="button"
              className="bg-yellow-400 text-gray-900 px-3 py-2 rounded cursor-pointer font-semibold hover:bg-yellow-300"
              onClick={() => duplicatesRef.current?.click()}
            >Browse</button>
            <input
              type="file"
              style={{ display: "none" }}
              ref={duplicatesRef}
              //@ts-ignore
              webkitdirectory="true"
              directory="true"
              onChange={e => {
                const files = e.target.files;
                if (files && files.length > 0) {
                  const relPath = files[0].webkitRelativePath;
                  const folderPath = relPath.substring(0, relPath.indexOf("/"));
                  setDuplicates(folderPath);
                }
              }}
            />
          </div>
        </div>
        <button type="submit" className="bg-yellow-400 text-gray-900 px-6 py-2 rounded font-bold hover:bg-yellow-300 transition">Save</button>
        {message && <div className="mt-2 text-green-400 font-semibold">{message}</div>}
      </form>
    </div>
  );
}
