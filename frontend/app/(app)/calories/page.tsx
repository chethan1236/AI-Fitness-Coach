"use client";
import { useState } from "react";
import { FaAppleAlt, FaFire, FaPlus } from "react-icons/fa";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { Input } from "@/components/ui/input";
import { useAppStore } from "@/store/app-store";

export default function CaloriesPage() {
  const [open, setOpen] = useState(false); const addToast = useAppStore((state) => state.addToast);
  return <><PageHeader title="Calorie tracker" description="A clear picture of today’s fuel and movement." action={<Button onClick={() => setOpen(true)}><FaPlus /> Log food</Button>} /><section className="grid gap-6 lg:grid-cols-[1fr_1.4fr]"><article className="panel grid place-items-center p-8 text-center"><div className="grid h-48 w-48 place-items-center rounded-full border-[14px] border-emerald-500/20 border-t-emerald-500"><div><p className="text-4xl font-bold">1,570</p><p className="text-sm text-slate-500">of 2,100 kcal</p></div></div><p className="mt-6 text-sm font-semibold text-emerald-600">530 calories remaining</p></article><article className="panel p-6"><h2 className="font-bold">Today’s balance</h2><div className="mt-6 grid gap-4 sm:grid-cols-3">{[["Food", "1,920", FaAppleAlt, "emerald"], ["Exercise", "350", FaFire, "sky"], ["Net", "1,570", FaFire, "violet"]].map(([label, value, Icon, tone]) => { const CardIcon = Icon as typeof FaFire; return <div key={label as string} className="rounded-2xl bg-slate-50 p-5 dark:bg-slate-800"><CardIcon className={tone === "emerald" ? "text-emerald-500" : tone === "sky" ? "text-sky-500" : "text-violet-500"} /><p className="mt-4 text-2xl font-bold">{value as string}</p><p className="text-sm text-slate-500">{label as string} calories</p></div>; })}</div><div className="mt-8"><div className="mb-2 flex justify-between text-sm"><span>Daily budget</span><span className="font-bold">75%</span></div><div className="h-3 rounded-full bg-slate-100 dark:bg-slate-800"><div className="h-3 w-3/4 rounded-full bg-gradient-to-r from-emerald-500 to-sky-500" /></div></div></article></section><Modal open={open} onClose={() => setOpen(false)} title="Log a meal"><div className="grid gap-4"><Input label="Food or meal" placeholder="e.g. Protein smoothie" /><Input label="Calories" type="number" placeholder="0" /><Button onClick={() => { setOpen(false); addToast({ title: "Meal logged", description: "Your daily total was updated." }); }}>Save meal</Button></div></Modal></>;
}
