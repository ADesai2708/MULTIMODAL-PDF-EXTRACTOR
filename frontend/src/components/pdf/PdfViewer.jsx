import { Document, Page } from "react-pdf";
import { useState } from "react";

function PdfViewer() {

  const [file] = useState(null);

  return (

    <div className="
      bg-white
      rounded-xl
      border
      border-slate-200
      h-1162.5
      overflow-auto
      p-4
    ">

      <h2 className="font-semibold mb-4">
        PDF Preview
      </h2>

      {!file ? (

        <div className="
          h-full
          flex
          items-center
          justify-center
          text-slate-400
        ">

          Upload a PDF to preview

        </div>

      ) : (

        <Document file={file}>
          <Page pageNumber={1}/>
        </Document>

      )}

    </div>

  );
}

export default PdfViewer;