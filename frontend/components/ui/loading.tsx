import { cn } from "@/lib/utils";

export function LoadingSpinner({ className }: { className?: string }) { return <span className={cn("inline-block h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent", className)} aria-label="Loading" />; }
export function SkeletonLoader({ className }: { className?: string }) { return <div className={cn("animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800", className)} />; }
