"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { FaChartLine, FaDumbbell, FaFire, FaLeaf, FaTimes, FaUser, FaCog, FaThLarge } from "react-icons/fa";
import { cn } from "@/lib/utils";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: FaThLarge }, { href: "/workouts", label: "Workout plans", icon: FaDumbbell },
  { href: "/diet", label: "Diet plans", icon: FaLeaf }, { href: "/calories", label: "Calories", icon: FaFire },
  { href: "/progress", label: "Progress", icon: FaChartLine }, { href: "/profile", label: "Profile", icon: FaUser }, { href: "/settings", label: "Settings", icon: FaCog },
];

export function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  const pathname = usePathname();
  return <><div className={cn("fixed inset-0 z-30 bg-slate-950/40 lg:hidden", open ? "block" : "hidden")} onClick={onClose} /><aside className={cn("fixed inset-y-0 left-0 z-40 flex w-72 -translate-x-full flex-col border-r bg-white p-5 transition-transform dark:bg-slate-950 lg:translate-x-0", open && "translate-x-0")}><div className="mb-9 flex items-center justify-between"><Link href="/dashboard" className="text-xl font-extrabold"><span className="gradient-text">AIFit</span> Coach</Link><button className="lg:hidden" onClick={onClose} aria-label="Close navigation"><FaTimes /></button></div><nav className="grid gap-1">{items.map(({ href, label, icon: Icon }) => <Link key={href} href={href} onClick={onClose} className={cn("flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-900 dark:hover:text-white", pathname === href && "bg-gradient-to-r from-emerald-500 to-sky-500 text-white shadow-lg shadow-emerald-500/20 hover:text-white")}><Icon className="text-base" />{label}</Link>)}</nav><div className="mt-auto rounded-2xl bg-gradient-to-br from-emerald-500 to-sky-500 p-4 text-white"><p className="text-sm font-bold">Ready for today?</p><p className="mt-1 text-xs text-white/80">Your next workout starts in 2 hours.</p></div></aside></>;
}
