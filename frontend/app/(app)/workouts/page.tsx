import { FaClock, FaPlay } from "react-icons/fa";
import { PageHeader } from "@/components/layout/page-header";
import { workouts } from "@/lib/mock-data";
import { Button } from "@/components/ui/button";

export default function WorkoutsPage() { return <><PageHeader title="Workout plans" description="AI-curated sessions for your current goal and recovery." action={<Button>Create a workout</Button>} /><div className="grid gap-5 lg:grid-cols-3">{workouts.map((workout, index) => <article className="panel overflow-hidden" key={workout.title}><div className={`flex h-36 items-end bg-gradient-to-br p-5 text-white ${workout.color}`}><span className="rounded-full bg-white/20 px-3 py-1 text-xs font-bold">Plan {index + 1}</span></div><div className="p-5"><h2 className="text-xl font-bold">{workout.title}</h2><p className="mt-2 text-sm text-slate-500">{workout.focus}</p><div className="my-5 flex gap-4 text-sm font-medium text-slate-600 dark:text-slate-300"><span className="flex items-center gap-2"><FaClock />{workout.duration}</span><span>{workout.level}</span></div><Button className="w-full"><FaPlay /> Start session</Button></div></article>)}</div></> }
