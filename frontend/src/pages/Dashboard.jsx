
import Navbar from "../components/layout/Navbar";
import Sidebar from "../components/layout/Sidebar";

import StatsCards from "../components/dashboard/StatsCards";
import UploadZone from "../components/dashboard/UploadZone";

import ChatPanel from "../components/chat/ChatPanel";

import PdfViewer from "../components/pdf/PdfViewer";

function Dashboard() {
  return (
    <div className="h-screen bg-slate-100">

      <Navbar />

      <div className="flex h-[calc(100vh-70px)]">

        <Sidebar />

        <main className="flex-1 overflow-auto p-6">

          <StatsCards />

          <div className="grid grid-cols-12 gap-6 mt-6">

            <div className="col-span-3">
              <UploadZone />
            </div>

            <div className="col-span-5">
              <ChatPanel />
            </div>

            <div className="col-span-4">
              <PdfViewer />
            </div>

          </div>

        </main>

      </div>

    </div>
  );
}

export default Dashboard;

