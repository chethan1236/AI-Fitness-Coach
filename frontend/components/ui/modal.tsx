"use client";
import { type ReactNode, useEffect } from "react";
import { FaTimes } from "react-icons/fa";
import { Button } from "./button";

export function Modal({ open, onClose, title, children }: { open: boolean; onClose: () => void; title: string; children: ReactNode }) {
  useEffect(() => { const close = (event: KeyboardEvent) => event.key === "Escape" && onClose(); window.addEventListener("keydown", close); return () => window.removeEventListener("keydown", close); }, [onClose]);
  if (!open) return null;
  return <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/50 p-4" onMouseDown={onClose}><section className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl dark:bg-slate-900" onMouseDown={(event) => event.stopPropagation()} role="dialog" aria-modal="true"><div className="mb-5 flex items-center justify-between"><h2 className="text-lg font-bold">{title}</h2><Button variant="ghost" size="icon" onClick={onClose}><FaTimes /></Button></div>{children}</section></div>;
}
