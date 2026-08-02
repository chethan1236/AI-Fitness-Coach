"use client";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { useAppStore } from "@/store/app-store";
import { useAuthStore } from "@/store/auth-store";
import { profileService } from "@/services/profileService";
import {
  dietPreferences,
  experienceLevels,
  fitnessGoals,
  genders,
  preferredWorkoutTimes,
} from "@/types/profile";
import type { ProfileUpdatePayload } from "@/types/profile";

const schema = z.object({
  name: z.string().min(2, "Enter your name"),
  age: z.preprocess((value) => {
    if (value === "" || value === undefined || value === null) return null;
    return Number(value);
  }, z.number().int().min(13, "Age must be at least 13").max(120, "Enter a valid age").nullable()),
  gender: z.preprocess((value) => (value === "" ? null : value), z.enum(genders).nullable()),
  height: z.preprocess((value) => {
    if (value === "" || value === undefined || value === null) return null;
    return Number(value);
  }, z.number().positive("Enter a valid height").max(300, "Enter a valid height").nullable()),
  weight: z.preprocess((value) => {
    if (value === "" || value === undefined || value === null) return null;
    return Number(value);
  }, z.number().positive("Enter a valid weight").max(700, "Enter a valid weight").nullable()),
  goal: z.preprocess((value) => (value === "" ? null : value), z.enum(fitnessGoals).nullable()),
  experience: z.preprocess((value) => (value === "" ? null : value), z.enum(experienceLevels).nullable()),
  workout_days: z.preprocess((value) => {
    if (value === "" || value === undefined || value === null) return null;
    return Number(value);
  }, z.number().int().min(0, "Enter a valid number").max(7, "Enter a valid number").nullable()),
  preferred_workout_time: z.preprocess((value) => (value === "" ? null : value), z.enum(preferredWorkoutTimes).nullable()),
  diet_preference: z.preprocess((value) => (value === "" ? null : value), z.enum(dietPreferences).nullable()),
  daily_calorie_goal: z.preprocess((value) => {
    if (value === "" || value === undefined || value === null) return null;
    return Number(value);
  }, z.number().int().min(0, "Enter a valid calorie goal").nullable()),
});

type ProfileFormValues = z.infer<typeof schema>;

export default function ProfilePage() {
  const addToast = useAppStore((state) => state.addToast);
  const { user, setUser } = useAuthStore();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProfileFormValues>({ resolver: zodResolver(schema) });

  useEffect(() => {
    if (user) {
      reset({
        name: user.name,
        age: user.age,
        gender: user.gender,
        height: user.height,
        weight: user.weight,
        goal: user.goal,
        experience: user.experience,
        workout_days: user.workout_days ?? null,
        preferred_workout_time: user.preferred_workout_time,
        diet_preference: user.diet_preference,
        daily_calorie_goal: user.daily_calorie_goal ?? null,
      });
      return;
    }

    profileService
      .getProfile()
      .then((profile) => {
        setUser(profile);
        reset({
          name: profile.name,
          age: profile.age,
          gender: profile.gender,
          height: profile.height,
          weight: profile.weight,
          goal: profile.goal,
          experience: profile.experience,
          workout_days: profile.workout_days ?? null,
          preferred_workout_time: profile.preferred_workout_time,
          diet_preference: profile.diet_preference,
          daily_calorie_goal: profile.daily_calorie_goal ?? null,
        });
      })
      .catch(() => {
        addToast({
          title: "Unable to load profile",
          description: "Please refresh and try again.",
          variant: "error",
        });
      });
  }, [user, reset, setUser, addToast]);

  const onSubmit = async (values: ProfileFormValues) => {
    try {
      const updated = await profileService.updateProfile(values as ProfileUpdatePayload);
      setUser(updated);
      addToast({ title: "Profile updated", description: "Your preferences were saved.", variant: "success" });
    } catch {
      addToast({ title: "Save failed", description: "Please try again later.", variant: "error" });
    }
  };

  return (
    <>
      <PageHeader title="Your profile" description="Keep your baseline up to date so plans stay relevant." />
      <section className="grid gap-6 lg:grid-cols-[260px_1fr]">
        <aside className="panel flex flex-col items-center p-7 text-center">
          <div className="grid h-24 w-24 place-items-center rounded-full bg-gradient-to-br from-emerald-500 to-sky-500 text-3xl font-bold text-white">
            {user?.name?.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase()}
          </div>
          <h2 className="mt-4 text-xl font-bold">{user?.name ?? "Profile"}</h2>
          <p className="text-sm text-slate-500">Update your workout and nutrition settings anytime.</p>
        </aside>

        <form onSubmit={handleSubmit(onSubmit)} className="panel p-6">
          <h2 className="text-lg font-bold">Profile settings</h2>
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <Input label="Name" error={errors.name?.message as string | undefined} {...register("name")} />
            <Input label="Age" type="number" error={errors.age?.message as string | undefined} {...register("age")} />
            <Select label="Gender" error={errors.gender?.message as string | undefined} {...register("gender")}> 
              <option value="">Select gender</option>
              {genders.map((option) => (
                <option key={option} value={option}>{option.replaceAll("_", " ")}</option>
              ))}
            </Select>
            <Input label="Height (cm)" type="number" error={errors.height?.message as string | undefined} {...register("height")} />
            <Input label="Weight (kg)" type="number" error={errors.weight?.message as string | undefined} {...register("weight")} />
            <Select label="Goal" error={errors.goal?.message as string | undefined} {...register("goal")}> 
              <option value="">Select goal</option>
              {fitnessGoals.map((option) => (
                <option key={option} value={option}>{option.replaceAll("_", " ")}</option>
              ))}
            </Select>
            <Select label="Experience" error={errors.experience?.message as string | undefined} {...register("experience")}> 
              <option value="">Select experience</option>
              {experienceLevels.map((option) => (
                <option key={option} value={option}>{option.replaceAll("_", " ")}</option>
              ))}
            </Select>
            <Input label="Workout days per week" type="number" error={errors.workout_days?.message as string | undefined} {...register("workout_days")} />
            <Select label="Preferred workout time" error={errors.preferred_workout_time?.message as string | undefined} {...register("preferred_workout_time")}> 
              <option value="">Select time</option>
              {preferredWorkoutTimes.map((option) => (
                <option key={option} value={option}>{option.replaceAll("_", " ")}</option>
              ))}
            </Select>
            <Select label="Diet preference" error={errors.diet_preference?.message as string | undefined} {...register("diet_preference")}> 
              <option value="">Select diet</option>
              {dietPreferences.map((option) => (
                <option key={option} value={option}>{option.replaceAll("_", " ")}</option>
              ))}
            </Select>
            <Input label="Daily calorie goal" type="number" error={errors.daily_calorie_goal?.message as string | undefined} {...register("daily_calorie_goal")} />
          </div>
          <Button className="mt-6" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Saving profile..." : "Save changes"}
          </Button>
        </form>
      </section>
    </>
  );
}
