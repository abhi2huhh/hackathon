import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";
import { Bookmark } from "lucide-react";
import { resourceApi } from "../services/resourceApi";
import { Input } from "../components/ui/Input";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { useDebouncedValue } from "../hooks/useDebouncedValue";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function ResourcesPage() {
  const [q, setQ] = useState("");
  const [subject, setSubject] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [type, setType] = useState("");
  const delayed = useDebouncedValue(q, 200);
  const qc = useQueryClient();
  const query = useQuery({
    queryKey: ["resources", delayed, subject, difficulty, type],
    queryFn: () => resourceApi.list({ q: delayed, subject, difficulty, type }),
  });
  const bookmark = useMutation({
    mutationFn: (id: number) => resourceApi.bookmark(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources"] }),
  });

  return (
    <div>
      <h1 className="font-display text-5xl">Resource library</h1>
      <div className="mt-6 grid gap-3 md:grid-cols-4">
        <Input placeholder="Search titles" value={q} onChange={(e) => setQ(e.target.value)} />
        <Input placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />
        <Input placeholder="Difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} />
        <Input placeholder="Type (COURSE, ARTICLE…)" value={type} onChange={(e) => setType(e.target.value)} />
      </div>
      {query.isError && <div className="mt-4"><ErrorNote message={(query.error as Error).message} /></div>}
      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {(query.data?.items || []).map((item: any) => (
          <Card key={item.id} className="relative">
            <button
              aria-label="Bookmark"
              className="absolute right-5 top-5 text-accent"
              onClick={() => bookmark.mutate(item.id)}
            >
              <Bookmark fill={item.bookmarked ? "currentColor" : "none"} />
            </button>
            <Badge>{item.resource_type}</Badge>
            <h2 className="mt-3 font-display text-2xl">
              <Link to={`/resources/${item.id}`}>{item.title}</Link>
            </h2>
            <p className="mt-2 text-sm text-mute">{item.description}</p>
            <p className="mt-3 text-xs text-bronze">
              {item.subject} · {item.difficulty}
            </p>
          </Card>
        ))}
      </div>
      {query.data && query.data.total === 0 && <p className="mt-8 text-mute">No resources matched those filters.</p>}
    </div>
  );
}
