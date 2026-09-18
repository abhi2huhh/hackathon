import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { resourceApi } from "../services/resourceApi";
import { Button } from "../components/ui/Button";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function ResourceDetailPage() {
  const { id } = useParams();
  const query = useQuery({
    queryKey: ["resource", id],
    queryFn: () => resourceApi.detail(Number(id)),
  });
  if (query.isError) return <ErrorNote message={(query.error as Error).message} />;
  if (!query.data) return null;
  const item = query.data;
  return (
    <div className="max-w-3xl">
      <p className="text-xs uppercase tracking-[0.2em] text-bronze">{item.resource_type}</p>
      <h1 className="mt-2 font-display text-5xl">{item.title}</h1>
      <p className="mt-4 text-mute">{item.description}</p>
      <p className="mt-3 text-sm">{item.subject} · {item.difficulty}</p>
      <a href={item.url} target="_blank" rel="noreferrer">
        <Button className="mt-6">Open original source</Button>
      </a>
    </div>
  );
}
