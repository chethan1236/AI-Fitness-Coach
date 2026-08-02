"use client";
import { useState, type ReactNode } from "react";
import { Navbar } from "./navbar";
import { Sidebar } from "./sidebar";
import { ToastNotifications } from "@/components/ui/toast-notifications";

export function AppShell({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return <div className="min-h-screen"><Sidebar open={open} onClose={() => setOpen(false)} /><div className="lg:pl-72"><Navbar onMenu={() => setOpen(true)} /><main className="mx-auto max-w-7xl p-4 sm:p-6 lg:p-8">{children}</main></div><ToastNotifications /></div>;
}
