import React, { useState } from "react";

type Props = {
  onFilter: (tags: string, face: string) => void;
};

const FilterPanel: React.FC<Props> = ({ onFilter }) => {
  const [tags, setTags] = useState("");
  const [face, setFace] = useState("");

  return (
    <div className="flex space-x-2 mb-4">
      <input
        type="text"
        placeholder="Tags"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        className="border p-2 rounded flex-1"
      />
      <input
        type="text"
        placeholder="Face"
        value={face}
        onChange={(e) => setFace(e.target.value)}
        className="border p-2 rounded flex-1"
      />
      <button
        onClick={() => onFilter(tags, face)}
        className="bg-blue-600 text-white px-4 rounded"
      >
        Apply
      </button>
    </div>
  );
};

export default FilterPanel;
