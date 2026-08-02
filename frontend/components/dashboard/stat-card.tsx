import { type IconType } from "react-icons";

export function StatCard({ label, value, trend, icon: Icon, tone = "emerald" }: { label: string; value: string; trend: string; icon: IconType; tone?: "emerald" | "sky" | "violet" | "orange" }) {
  const tones = { emerald: "bg-emerald-500/10 text-emerald-500", sky: "bg-sky-500/10 text-sky-500", violet: "bg-violet-500/10 text-violet-500", orange: "bg-orange-500/10 text-orange-500" };
  return <article className="panel p-5"><div className="mb-5 flex items-start justify-between"><div><p className="text-sm font-medium text-slate-500">{label}</p><p className="mt-1 text-2xl font-bold">{value}</p></div><span className={`grid h-10 w-10 place-items-center rounded-xl ${tones[tone]}`}><Icon /></span></div><p className="text-xs font-semibold text-emerald-500">{trend}</p></article>;
}
