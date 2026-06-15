
import {
  FileText,
  FolderOpen
} from "lucide-react";

function Sidebar() {

  const documents = [
    "IEEE_Template.pdf",
    "Research_Paper.pdf",
    "Machine_Learning.pdf"
  ];

  return (
    <div
      className="
        w-65
        bg-white
        border-r
        border-slate-200
        p-5
      "
    >

      <div className="flex items-center gap-2 mb-6">

        <FolderOpen
          size={20}
          className="text-blue-600"
        />

        <h2 className="font-semibold">
          Documents
        </h2>

      </div>

      <div className="space-y-2">

        {documents.map((doc) => (

          <div
            key={doc}
            className="
              flex
              items-center
              gap-2
              p-3
              rounded-lg
              hover:bg-slate-100
              cursor-pointer
            "
          >

            <FileText size={18} />

            <span className="text-sm">
              {doc}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Sidebar;

