import { type ReactNode } from "react";

export function PageHeader({ eyebrow, title, description, action }: { eyebrow?: string; title: string; description: string; action?: ReactNode }) {
  return <header className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><p className="mb-1 text-xs font-bold uppercase tracking-[0.2em] text-emerald-500">{eyebrow ?? "AI Fitness Coach"}</p><h1 className="text-3xl font-bold tracking-tight">{title}</h1><p className="mt-1 text-slate-500 dark:text-slate-400">{description}</p></div>{action}</header>;
}
