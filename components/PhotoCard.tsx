import React from "react";

type Props = {
  filename: string;
  filepath: string;
  date_taken: string;
  tags?: string | null;
};

const PhotoCard: React.FC<Props> = ({ filename, filepath, date_taken, tags }) => {
  return (
    <div className="bg-white rounded shadow overflow-hidden">
      <img
        src={`file://${filepath}`}
        alt={filename}
        className="object-cover w-full h-64"
      />
      <div className="p-2">
        <div className="font-semibold">{filename}</div>
        <div className="text-xs text-gray-500">{date_taken}</div>
        {tags && <div className="text-xs mt-1 text-gray-700">Tags: {tags}</div>}
      </div>
    </div>
  );
};

export default PhotoCard;
