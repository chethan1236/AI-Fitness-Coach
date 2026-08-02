import { type InputHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> { label?: string; error?: string; }
export const Input = forwardRef<HTMLInputElement, InputProps>(({ className, label, error, id, ...props }, ref) => (
  <label className="grid gap-1.5 text-sm font-medium text-slate-700 dark:text-slate-200">
    {label && <span>{label}</span>}
    <input id={id} ref={ref} className={cn("h-11 rounded-xl border bg-white px-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 dark:bg-slate-900 dark:text-white", error && "border-rose-500", className)} {...props} />
    {error && <span className="text-xs font-normal text-rose-500">{error}</span>}
  </label>
));
Input.displayName = "Input";
