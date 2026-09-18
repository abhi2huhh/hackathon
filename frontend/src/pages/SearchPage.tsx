import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import { Input } from "../components/ui/Input";
import { useDebouncedValue } from "../hooks/useDebouncedValue";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function SearchPage() {
  const [q, setQ] = useState("python");
  const delayed = useDebouncedValue(q, 250);
  const query = useQuery({
    queryKey: ["search", delayed],
    queryFn: () => api<any>(`/search?q=${encodeURIComponent(delayed)}`),
    enabled: delayed.length >= 2,
  });

  return (
    <div>
      <h1 className="font-display text-5xl">Search the atelier</h1>
      <Input className="mt-6 max-w-xl" value={q} onChange={(e) => setQ(e.target.value)} />
      {query.isError && <div className="mt-4"><ErrorNote message={(query.error as Error).message} /></div>}
      {query.data && (
        <div className="mt-8 grid gap-6 md:grid-cols-2">
          {["roadmaps", "resources", "job_roles", "documents"].map((key) => (
            <section key={key} className="rounded-3xl border border-line p-5">
              <h2 className="font-display text-2xl capitalize">{key.replace("_", " ")}</h2>
              <ul className="mt-3 space-y-2 text-sm">
                {(query.data[key] || []).map((item: any) => (
                  <li key={item.id}>
                    {key === "roadmaps" ? (
                      <Link to={`/roadmaps/${item.id}`}>{item.title}</Link>
                    ) : key === "resources" ? (
                      <Link to={`/resources/${item.id}`}>{item.title}</Link>
                    ) : (
                      item.title
                    )}
                  </li>
                ))}
                {(query.data[key] || []).length === 0 && <li className="text-mute">No matches.</li>}
              </ul>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}
