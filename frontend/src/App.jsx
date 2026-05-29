import React, { useState } from 'react';
import { Upload, Search, FileText, Image as ImageIcon, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';

function App() {
  // Ingestion States
  const [pdfPath, setPdfPath] = useState('');
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState(null);

  // Query States
  const [question, setQuestion] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const [ragResponse, setRagResponse] = useState(null);

  // Handle Document Processing Request
  const handleIngestion = async (e) => {
    e.preventDefault();
    if (!pdfPath.strip) return;
    
    setIsIngesting(true);
    setIngestStatus(null);
    try {
      const res = await fetch('http://localhost:8000/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdf_path: pdfPath.trim() })
      });
      const data = await res.json();
      if (res.ok) {
        setIngestStatus({ type: 'success', message: data.message });
      } else {
        setIngestStatus({ type: 'error', message: data.detail || 'Ingestion failed' });
      }
    } catch (err) {
      setIngestStatus({ type: 'error', message: 'Could not connect to backend server.' });
    } finally {
      setIsIngesting(false);
    }
  };

  // Handle RAG Search Question
  const handleQuery = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsQuerying(true);
    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
      });
      const data = await res.json();
      if (res.ok) {
        setRagResponse(data);
      } else {
        alert('Query Error: ' + data.detail);
      }
    } catch (err) {
      alert('Failed to execute search context.');
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Top Banner Navigation */}
      <header className="bg-slate-900 text-white shadow-md px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <FileText className="h-6 w-6 text-emerald-400" />
          <h1 className="text-xl font-bold tracking-tight">Multi-Modal Research Paper Deep-Dive</h1>
        </div>
        <span className="text-xs bg-slate-800 px-3 py-1 rounded-full border border-slate-700 text-slate-300 font-mono">
          Engine: BLIP Local Core
        </span>
      </header>

      {/* Main Workspace Split View */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Left Column: Management Configuration */}
        <div className="md:col-span-1 space-y-6">
          <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-base font-semibold text-slate-800 mb-3 flex items-center gap-2">
              <Upload className="w-4 h-4 text-slate-500" /> Document Ingestion Layer
            </h2>
            <p className="text-xs text-slate-500 mb-4">
              Enter the path of your patent/IEEE paper file to run layout markdown segmentation and figure extraction.
            </p>
            
            <form onSubmit={handleIngestion} className="space-y-3">
              <input
                type="text"
                className="w-full text-sm px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 font-mono"
                placeholder="e.g. C:/data/sample.pdf"
                value={pdfPath}
                onChange={(e) => setPdfPath(e.target.value)}
                disabled={isIngesting}
              />
              <button
                type="submit"
                disabled={isIngesting || !pdfPath}
                className="w-full bg-slate-900 text-white text-sm font-medium py-2 rounded-lg hover:bg-slate-800 transition flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {isIngesting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-emerald-400" /> Ingesting & Segmenting...
                  </>
                ) : 'Run Multi-Modal Ingest'}
              </button>
            </form>

            {/* Ingestion Status Alert Box */}
            {ingestStatus && (
              <div className={`mt-4 p-3 rounded-lg flex items-start gap-2 text-xs ${
                ingestStatus.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'
              }`}>
                {ingestStatus.type === 'success' ? <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" /> : <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />}
                <span>{ingestStatus.message}</span>
              </div>
            )}
          </div>
        </div>

        {/* Right Column Canvas: Search and Results Visualizer */}
        <div className="md:col-span-2 flex flex-col space-y-6">
          {/* Ask Query Box */}
          <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <form onSubmit={handleQuery} className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                <input
                  type="text"
                  className="w-full text-sm pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ask a question about layout structures, tables, or data charts..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  disabled={isQuerying}
                />
              </div>
              <button
                type="submit"
                disabled={isQuerying || !question}
                className="bg-blue-600 text-white text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-50"
              >
                {isQuerying ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Query'}
              </button>
            </form>
          </div>

          {/* Core Response Canvas Dashboard */}
          {ragResponse && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
              {/* Answer Space Block */}
              <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col">
                <h3 className="text-sm font-semibold text-slate-700 border-b border-slate-100 pb-2 mb-3">
                  Synthesized Answer Payload
                </h3>
                <div className="text-sm text-slate-800 leading-relaxed whitespace-pre-wrap flex-1">
                  {ragResponse.answer}
                </div>
              </div>

              {/* Side Graphical Panel Evidence Map */}
              <div className="lg:col-span-1 bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex flex-col">
                <h3 className="text-sm font-semibold text-slate-700 border-b border-slate-100 pb-2 mb-3 flex items-center gap-1.5">
                  <ImageIcon className="w-4 h-4 text-blue-500" /> Grounded Evidence
                </h3>
                {ragResponse.referenced_images?.length > 0 ? (
                  <div className="space-y-4 overflow-y-auto max-h-[450px] pr-1">
                    {ragResponse.referenced_images.map((img, idx) => (
                      <div key={idx} className="border border-slate-200 rounded-lg overflow-hidden bg-slate-50 shadow-xs">
                        <div className="bg-slate-100 px-2 py-1 text-[10px] text-slate-600 border-b border-slate-200 truncate font-mono">
                          {img.name}
                        </div>
                        <img 
                          src={img.url} 
                          alt={img.name} 
                          className="w-full h-auto object-contain bg-white max-h-48"
                          onError={(e) => { e.target.src = 'https://placehold.co/300x200?text=Image+Load+Error'; }}
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex-1 flex flex-col items-center justify-center text-slate-400 p-4 text-center">
                    <ImageIcon className="w-8 h-8 stroke-1 text-slate-300 mb-2" />
                    <p className="text-xs">No visual figures matched this text search context.</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;