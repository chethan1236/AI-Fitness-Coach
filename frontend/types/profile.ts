export const genders = ["male", "female", "non_binary", "prefer_not_to_say"] as const;
export const fitnessGoals = ["lose_weight", "build_muscle", "improve_fitness", "maintain_health"] as const;
export const experienceLevels = ["beginner", "intermediate", "advanced"] as const;
export const preferredWorkoutTimes = ["morning", "afternoon", "evening", "night"] as const;
export const dietPreferences = ["balanced", "low_carb", "high_protein", "vegetarian", "vegan", "paleo", "keto"] as const;

export type Gender = (typeof genders)[number];
export type FitnessGoal = (typeof fitnessGoals)[number];
export type ExperienceLevel = (typeof experienceLevels)[number];
export type PreferredWorkoutTime = (typeof preferredWorkoutTimes)[number];
export type DietPreference = (typeof dietPreferences)[number];

export type ProfileUpdatePayload = {
  name: string;
  age: number | null;
  gender: Gender | null;
  height: number | null;
  weight: number | null;
  goal: FitnessGoal | null;
  experience: ExperienceLevel | null;
  workout_days: number;
  preferred_workout_time: PreferredWorkoutTime;
  diet_preference: DietPreference;
  daily_calorie_goal: number;
};
