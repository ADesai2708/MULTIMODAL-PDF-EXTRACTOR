
import { useState } from "react";
import { UploadCloud } from "lucide-react";

function UploadZone() {
const [loading, setLoading] =
useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {

    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);
  };

  return (
    <div
      className="
        bg-white
        rounded-xl
        border
        border-slate-200
        p-6
        h-125
      "
    >

      <h2 className="font-semibold text-lg mb-4">
        Upload Document
      </h2>
      <button
  className="
    mt-6
    w-full
    bg-blue-600
    text-white
    py-3
    rounded-lg
  "
>
  Index Document
</button>

      <label
        className="
          border-2
          border-dashed
          border-slate-300
          rounded-xl
          flex
          flex-col
          items-center
          justify-center
          h-62.5
          cursor-pointer
          hover:border-blue-500
          transition
        "
      >

        <UploadCloud
          size={40}
          className="text-blue-600"
        />

        <p className="mt-4 text-slate-600">
          Click to select PDF
        </p>

        <input
          type="file"
          accept=".pdf"
          hidden
          onChange={handleFileChange}
        />

      </label>

      {selectedFile && (

        <div className="mt-6">

          <p className="font-medium">
            Selected File
          </p>

          <p className="text-sm text-slate-500 mt-2">
            {selectedFile.name}
          </p>

        </div>

      )}

    </div>
  );
}

export default UploadZone;
