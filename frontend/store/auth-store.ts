"use client";
import { create } from "zustand";
import { clearAuthTokens, getRefreshToken, setAuthTokens } from "@/lib/auth";
import { authService } from "@/services/authService";
import type { LoginPayload, RegisterPayload, TokenPair, User } from "@/types/auth";

type AuthState = {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  initialize: () => Promise<void>;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => Promise<void>;
  applyTokens: (tokens: TokenPair) => void;
  clearSession: () => void;
  setUser: (user: User | null) => void;
};

function message(error: unknown) {
  const detail = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
  return typeof detail === "string" ? detail : "Something went wrong. Please try again.";
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null, accessToken: null, refreshToken: null, isAuthenticated: false, loading: true, error: null,
  applyTokens: (tokens) => { setAuthTokens(tokens); set({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token }); },
  setUser: (user) => set({ user }),
  clearSession: () => { clearAuthTokens(); set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false, loading: false, error: null }); },
  initialize: async () => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) { set({ loading: false }); return; }
    set({ loading: true, error: null });
    try {
      const tokens = await authService.refresh(refreshToken);
      get().applyTokens(tokens);
      const user = await authService.getMe();
      set({ user, isAuthenticated: true, loading: false });
    } catch { get().clearSession(); }
  },
  login: async (payload) => {
    set({ loading: true, error: null });
    try {
      const tokens = await authService.login(payload);
      get().applyTokens(tokens);
      const user = await authService.getMe();
      set({ user, isAuthenticated: true, loading: false });
    } catch (error) { clearAuthTokens(); set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false, loading: false, error: message(error) }); throw error; }
  },
  register: async (payload) => {
    set({ loading: true, error: null });
    try { await authService.register(payload); await get().login({ email: payload.email, password: payload.password }); }
    catch (error) { set({ loading: false, error: message(error) }); throw error; }
  },
  logout: async () => {
    const refreshToken = get().refreshToken ?? getRefreshToken();
    try { if (refreshToken) await authService.logout(refreshToken); } finally { get().clearSession(); }
  },
}));
