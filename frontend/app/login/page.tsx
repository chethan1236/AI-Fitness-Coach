"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ToastNotifications } from "@/components/ui/toast-notifications";
import { useAppStore } from "@/store/app-store";
import { useAuthStore } from "@/store/auth-store";

const schema = z.object({ email: z.string().email("Enter a valid email"), password: z.string().min(8, "Use at least 8 characters") });
type FormValues = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const addToast = useAppStore((state) => state.addToast);
  const { login, loading, error } = useAuthStore();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const onSubmit = async (values: FormValues) => { try { await login(values); addToast({ title: "Welcome back", description: "Your fitness dashboard is ready." }); router.push("/dashboard"); } catch { /* Error is shown from the store. */ } };
  return <main className="grid min-h-screen place-items-center bg-slate-950 p-5"><ToastNotifications /><section className="w-full max-w-md rounded-3xl border border-white/10 bg-white p-8 shadow-2xl dark:bg-slate-900"><Link href="/" className="text-xl font-extrabold"><span className="gradient-text">AIFit</span> Coach</Link><p className="mt-8 text-3xl font-bold">Welcome back</p><p className="mt-2 text-slate-500">Sign in to continue your healthy streak.</p><form onSubmit={handleSubmit(onSubmit)} className="mt-7 grid gap-4"><Input label="Email" type="email" autoComplete="email" error={errors.email?.message} {...register("email")} /><Input label="Password" type="password" autoComplete="current-password" error={errors.password?.message} {...register("password")} />{error && <p role="alert" className="text-sm text-rose-500">{error}</p>}<Button type="submit" disabled={isSubmitting || loading}>{isSubmitting || loading ? "Signing in..." : "Sign in"}</Button></form><p className="mt-6 text-center text-sm text-slate-500">New to AIFit? <Link href="/register" className="font-bold text-emerald-600">Create an account</Link></p></section></main>;
}
