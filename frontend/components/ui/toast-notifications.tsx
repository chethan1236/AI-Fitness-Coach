"use client";
import { FaCheckCircle, FaTimes, FaTimesCircle } from "react-icons/fa";
import { useAppStore } from "@/store/app-store";

export function ToastNotifications() {
  const { toasts, dismissToast } = useAppStore();
  return <div className="fixed right-4 top-4 z-[60] grid w-[min(24rem,calc(100vw-2rem))] gap-2">{toasts.map((toast) => <div key={toast.id} className="flex gap-3 rounded-xl border bg-white p-4 shadow-xl dark:bg-slate-900"><span className={toast.variant === "error" ? "text-rose-500" : "text-emerald-500"}>{toast.variant === "error" ? <FaTimesCircle /> : <FaCheckCircle />}</span><div className="flex-1"><p className="font-semibold">{toast.title}</p>{toast.description && <p className="text-sm text-slate-500">{toast.description}</p>}</div><button onClick={() => dismissToast(toast.id)} aria-label="Dismiss"><FaTimes /></button></div>)}</div>;
}
