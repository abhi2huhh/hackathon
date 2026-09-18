import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { roadmapApi } from "../services/roadmapApi";
import { Button } from "../components/ui/Button";
import { ErrorNote } from "../components/ui/ErrorNote";
import { Skeleton } from "../components/loaders/Skeleton";

export default function RoadmapDetailPage() {
  const { id } = useParams();
  const qc = useQueryClient();
  const query = useQuery({
    queryKey: ["roadmap", id],
    queryFn: () => roadmapApi.detail(Number(id)),
  });
  const mutation = useMutation({
    mutationFn: (payload: { step_id: number; completed: boolean }) =>
      roadmapApi.progress(Number(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["roadmap", id] }),
  });
  if (query.isLoading) return <Skeleton className="h-64" />;
  if (query.isError) return <ErrorNote message={(query.error as Error).message} />;
  const data = query.data;
  const done = new Set(data.progress?.completed_step_ids || []);

  return (
    <div>
      <p className="text-xs uppercase tracking-[0.28em] text-bronze">{data.difficulty}</p>
      <h1 className="mt-2 font-display text-5xl">{data.title}</h1>
      <p className="mt-3 max-w-2xl text-mute">{data.description}</p>
      <div className="mt-4 h-2 overflow-hidden rounded-full bg-line">
        <div className="h-full bg-accent" style={{ width: `${data.progress?.percent || 0}%` }} />
      </div>
      <ol className="mt-10 space-y-5">
        {(data.steps || []).map((step: any) => (
          <li key={step.id} className="rounded-3xl border border-line bg-panel p-6">
            <p className="text-xs uppercase tracking-[0.2em] text-bronze">{step.stage}</p>
            <h2 className="mt-1 font-display text-3xl">{step.title}</h2>
            <p className="mt-2 text-mute">{step.description}</p>
            <Button
              className="mt-4"
              variant={done.has(step.id) ? "primary" : "line"}
              onClick={() => mutation.mutate({ step_id: step.id, completed: !done.has(step.id) })}
            >
              {done.has(step.id) ? "Completed" : "Mark complete"}
            </Button>
          </li>
        ))}
      </ol>
    </div>
  );
}
