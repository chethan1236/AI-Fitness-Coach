export type User = {
  id: string;
  name: string;
  email: string;
  age: number | null;
  gender: "male" | "female" | "non_binary" | "prefer_not_to_say" | null;
  height: number | null;
  weight: number | null;
  goal: "lose_weight" | "build_muscle" | "improve_fitness" | "maintain_health" | null;
  experience: "beginner" | "intermediate" | "advanced" | null;
  workout_days: number | null;
  preferred_workout_time: "morning" | "afternoon" | "evening" | "night" | null;
  diet_preference: "balanced" | "low_carb" | "high_protein" | "vegetarian" | "vegan" | "paleo" | "keto" | null;
  daily_calorie_goal: number | null;
  created_at: string;
  updated_at: string;
};

export type TokenPair = { access_token: string; refresh_token: string; token_type: "bearer" };
export type LoginPayload = { email: string; password: string };
export type RegisterPayload = LoginPayload & { name: string };
