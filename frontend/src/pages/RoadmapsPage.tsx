import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { roadmapApi } from "../services/roadmapApi";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Skeleton } from "../components/loaders/Skeleton";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function RoadmapsPage() {
  const query = useQuery({ queryKey: ["roadmaps"], queryFn: roadmapApi.list });
  if (query.isLoading) return <Skeleton className="h-40" />;
  if (query.isError) return <ErrorNote message={(query.error as Error).message} />;
  return (
    <div>
      <h1 className="font-display text-5xl">Learning journeys</h1>
      <div className="mt-8 grid gap-5 md:grid-cols-2">
        {(query.data || []).map((item: any) => (
          <Link key={item.id} to={`/roadmaps/${item.id}`}>
            <Card className="h-full transition hover:-translate-y-1">
              <Badge>{item.difficulty}</Badge>
              <h2 className="mt-3 font-display text-3xl">{item.title}</h2>
              <p className="mt-2 text-sm text-mute">{item.description}</p>
              <p className="mt-4 text-xs text-bronze">{item.estimated_duration}</p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
