"use client";

import { create } from "zustand";

type Toast = { id: number; title: string; description?: string; variant?: "success" | "error" };

type AppState = {
  darkMode: boolean;
  toasts: Toast[];
  toggleDarkMode: () => void;
  addToast: (toast: Omit<Toast, "id">) => void;
  dismissToast: (id: number) => void;
};

export const useAppStore = create<AppState>((set) => ({
  darkMode: false,
  toasts: [],
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
  addToast: (toast) => {
    const id = Date.now();
    set((state) => ({ toasts: [...state.toasts, { ...toast, id }] }));
    window.setTimeout(() => set((state) => ({ toasts: state.toasts.filter((item) => item.id !== id) })), 3500);
  },
  dismissToast: (id) => set((state) => ({ toasts: state.toasts.filter((item) => item.id !== id) })),
}));
