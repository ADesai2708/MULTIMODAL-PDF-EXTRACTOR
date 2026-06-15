
import {
  FileText,
  Image,
  Database,
  MessageSquare
} from "lucide-react";

const stats = [
  {
    title: "Documents",
    value: "12",
    icon: FileText
  },
  {
    title: "Images",
    value: "48",
    icon: Image
  },
  {
    title: "Chunks",
    value: "320",
    icon: Database
  },
  {
    title: "Queries",
    value: "95",
    icon: MessageSquare
  }
];

function StatsCards() {
  return (
    <div className="grid grid-cols-4 gap-5">

      {stats.map((stat) => {

        const Icon = stat.icon;

        return (
          <div
            key={stat.title}
            className="
              bg-white
              rounded-xl
              border
              border-slate-200
              p-5
              shadow-sm
            "
          >

            <div className="flex justify-between items-center">

              <div>

                <p className="text-slate-500 text-sm">
                  {stat.title}
                </p>

                <h2 className="text-3xl font-bold mt-2">
                  {stat.value}
                </h2>

              </div>

              <Icon
                size={28}
                className="text-blue-600"
              />

            </div>

          </div>
        );
      })}
    </div>
  );
}

export default StatsCards;
