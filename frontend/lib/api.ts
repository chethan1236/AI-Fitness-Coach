import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";
import { clearAuthTokens, getAccessToken, getRefreshToken, setAuthTokens } from "@/lib/auth";
import type { TokenPair } from "@/types/auth";

const baseURL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export const api = axios.create({ baseURL, headers: { "Content-Type": "application/json" } });
const refreshApi = axios.create({ baseURL, headers: { "Content-Type": "application/json" } });

type RetriableRequest = InternalAxiosRequestConfig & { _retry?: boolean };
let refreshPromise: Promise<TokenPair> | null = null;

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

async function syncRefreshedTokens(tokens: TokenPair) {
  setAuthTokens(tokens);
  const { useAuthStore } = await import("@/store/auth-store");
  useAuthStore.getState().applyTokens(tokens);
}

async function endSession() {
  clearAuthTokens();
  const { useAuthStore } = await import("@/store/auth-store");
  useAuthStore.getState().clearSession();
  if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) window.location.assign("/login");
}

async function refreshAccessToken(): Promise<TokenPair> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) throw new Error("No refresh token is available");
  if (!refreshPromise) {
    refreshPromise = refreshApi.post<TokenPair>("/api/v1/auth/refresh", { refresh_token: refreshToken })
      .then(({ data }) => syncRefreshedTokens(data).then(() => data))
      .catch(async (error) => { await endSession(); throw error; })
      .finally(() => { refreshPromise = null; });
  }
  return refreshPromise;
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const request = error.config as RetriableRequest | undefined;
    const path = request?.url ?? "";
    const isPublicAuthRequest = ["/auth/login", "/auth/register", "/auth/refresh"].some((route) => path.includes(route));
    if (error.response?.status !== 401 || !request || request._retry || isPublicAuthRequest) return Promise.reject(error);
    request._retry = true;
    try {
      const tokens = await refreshAccessToken();
      request.headers.Authorization = `Bearer ${tokens.access_token}`;
      return api(request);
    } catch {
      return Promise.reject(error);
    }
  },
);
