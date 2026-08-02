import type { TokenPair } from "@/types/auth";

const REFRESH_TOKEN_KEY = "aifit.refresh-token";
let accessToken: string | null = null;

export function getAccessToken() { return accessToken; }
export function getRefreshToken() { return typeof window === "undefined" ? null : window.sessionStorage.getItem(REFRESH_TOKEN_KEY); }

export function setAuthTokens(tokens: TokenPair) {
  accessToken = tokens.access_token;
  if (typeof window !== "undefined") window.sessionStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

export function clearAuthTokens() {
  accessToken = null;
  if (typeof window !== "undefined") window.sessionStorage.removeItem(REFRESH_TOKEN_KEY);
}
