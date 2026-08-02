import { api } from "@/lib/api";
import type { LoginPayload, RegisterPayload, TokenPair, User } from "@/types/auth";

export const authService = {
  async register(payload: RegisterPayload) { return (await api.post<User>("/api/v1/auth/register", payload)).data; },
  async login(payload: LoginPayload) { return (await api.post<TokenPair>("/api/v1/auth/login", payload)).data; },
  async refresh(refreshToken: string) { return (await api.post<TokenPair>("/api/v1/auth/refresh", { refresh_token: refreshToken })).data; },
  async logout(refreshToken: string) { await api.post("/api/v1/auth/logout", { refresh_token: refreshToken }); },
  async getMe() { return (await api.get<User>("/api/v1/users/me")).data; },
};
