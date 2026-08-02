"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { FaBars, FaBell, FaMoon, FaSignOutAlt, FaSun } from "react-icons/fa";
import { Button } from "@/components/ui/button";
import { useAppStore } from "@/store/app-store";
import { useAuthStore } from "@/store/auth-store";

export function Navbar({ onMenu }: { onMenu: () => void }) {
  const router = useRouter();
  const { darkMode, toggleDarkMode, addToast } = useAppStore();
  const { user, logout } = useAuthStore();
  useEffect(() => { document.documentElement.classList.toggle("dark", darkMode); }, [darkMode]);
  const handleLogout = async () => { try { await logout(); } finally { addToast({ title: "Signed out", description: "Your session has been closed." }); router.push("/login"); } };
  const initials = user?.name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase() ?? "AF";
  return <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b bg-slate-50/85 px-4 backdrop-blur dark:bg-slate-950/85 lg:px-8"><div className="flex items-center gap-3"><Button variant="ghost" size="icon" className="lg:hidden" onClick={onMenu}><FaBars /></Button><div><p className="text-sm font-semibold">Good morning, {user?.name.split(" ")[0] ?? "there"}</p><p className="text-xs text-slate-500">Let&apos;s make progress today.</p></div></div><div className="flex items-center gap-2"><Button variant="ghost" size="icon" onClick={toggleDarkMode} aria-label="Toggle dark mode">{darkMode ? <FaSun /> : <FaMoon />}</Button><Button variant="ghost" size="icon" aria-label="Notifications"><FaBell /></Button><Button variant="ghost" size="icon" onClick={() => void handleLogout()} aria-label="Sign out"><FaSignOutAlt /></Button><div className="ml-1 grid h-10 w-10 place-items-center rounded-full bg-gradient-to-br from-emerald-500 to-sky-500 text-sm font-bold text-white">{initials}</div></div></header>;
}
