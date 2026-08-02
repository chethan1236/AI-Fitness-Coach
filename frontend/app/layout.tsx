import type { Metadata } from "next";
import "../styles/globals.css";
import { AuthProvider } from "@/components/providers/auth-provider";

export const metadata: Metadata = {
  title: "AI Fitness Coach",
  description: "Your AI-powered fitness companion"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" suppressHydrationWarning><body><AuthProvider>{children}</AuthProvider></body></html>;
}
