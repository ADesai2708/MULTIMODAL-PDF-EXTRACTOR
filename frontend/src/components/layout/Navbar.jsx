
import { Search } from "lucide-react";

function Navbar() {
  return (
    <div className="h-17.5 bg-white border-b border-slate-200 flex items-center justify-between px-8">

      <div>

        <h1 className="text-2xl font-bold text-slate-800">
          Muiltimodal PDF
        </h1>

      </div>

      <div className="w-87.5">

        <div className="relative">

          <Search
            size={18}
            className="absolute top-3 left-3 text-slate-400"
          />

          <input
            placeholder="Search documents..."
            className="w-full bg-slate-100 rounded-lg py-2 pl-10 pr-4 outline-none"
          />

        </div>

      </div>

    </div>
  );
}

export default Navbar;

