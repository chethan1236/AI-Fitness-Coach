"use client";
import { useEffect, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import { LoadingSpinner } from "@/components/ui/loading";
import { useAuthStore } from "@/store/auth-store";

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuthStore();
  useEffect(() => { if (!loading && !isAuthenticated) router.replace("/login"); }, [isAuthenticated, loading, router]);
  if (loading || !isAuthenticated) return <div className="grid min-h-screen place-items-center"><LoadingSpinner className="h-8 w-8 text-emerald-500" /></div>;
  return <>{children}</>;
}
