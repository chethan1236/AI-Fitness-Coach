"use client";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function GlobalError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) { useEffect(() => { console.error(error); }, [error]); return <main className="grid min-h-screen place-items-center p-6 text-center"><div><p className="text-3xl font-bold">Something went wrong</p><p className="mt-2 text-slate-500">Please try loading this page again.</p><Button className="mt-6" onClick={reset}>Try again</Button></div></main>; }
