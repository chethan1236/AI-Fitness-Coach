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

const schema = z.object({ name: z.string().min(2, "Tell us your name"), email: z.string().email("Enter a valid email"), password: z.string().min(8, "Use at least 8 characters") });
type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const router = useRouter();
  const addToast = useAppStore((state) => state.addToast);
  const { register: createAccount, loading, error } = useAuthStore();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const onSubmit = async (values: FormValues) => { try { await createAccount(values); addToast({ title: `Welcome, ${values.name}`, description: "Your account and session are ready." }); router.push("/dashboard"); } catch { /* Error is shown from the store. */ } };
  return <main className="grid min-h-screen place-items-center bg-slate-950 p-5"><ToastNotifications /><section className="w-full max-w-md rounded-3xl border border-white/10 bg-white p-8 shadow-2xl dark:bg-slate-900"><Link href="/" className="text-xl font-extrabold"><span className="gradient-text">AIFit</span> Coach</Link><p className="mt-8 text-3xl font-bold">Start your journey</p><p className="mt-2 text-slate-500">A smarter routine starts with one small step.</p><form onSubmit={handleSubmit(onSubmit)} className="mt-7 grid gap-4"><Input label="Your name" autoComplete="name" error={errors.name?.message} {...register("name")} /><Input label="Email" type="email" autoComplete="email" error={errors.email?.message} {...register("email")} /><Input label="Password" type="password" autoComplete="new-password" error={errors.password?.message} {...register("password")} />{error && <p role="alert" className="text-sm text-rose-500">{error}</p>}<Button type="submit" disabled={isSubmitting || loading}>{isSubmitting || loading ? "Creating account..." : "Create my plan"}</Button></form><p className="mt-6 text-center text-sm text-slate-500">Already a member? <Link href="/login" className="font-bold text-emerald-600">Sign in</Link></p></section></main>;
}
