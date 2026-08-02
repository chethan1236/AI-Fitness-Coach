import { api } from "@/lib/api";
import type { ProfileUpdatePayload } from "@/types/profile";
import type { User } from "@/types/auth";

export const profileService = {
  async getProfile(): Promise<User> {
    return (await api.get<User>("/api/v1/users/me")).data;
  },

  async updateProfile(payload: ProfileUpdatePayload): Promise<User> {
    return (await api.patch<User>("/api/v1/users/me", payload)).data;
  },
};
