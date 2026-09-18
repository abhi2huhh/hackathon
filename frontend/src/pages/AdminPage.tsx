import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { Card } from "../components/ui/Card";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function AdminPage() {
  const stats = useQuery({ queryKey: ["admin-stats"], queryFn: () => api<any>("/admin/stats") });
  const users = useQuery({ queryKey: ["admin-users"], queryFn: () => api<any[]>("/admin/users") });
  if (stats.isError) return <ErrorNote message={(stats.error as Error).message} />;
  return (
    <div>
      <h1 className="font-display text-5xl">Stewardship</h1>
      <div className="mt-8 grid gap-4 md:grid-cols-5">
        {Object.entries(stats.data || {}).map(([k, v]) => (
          <Card key={k}>
            <p className="text-xs uppercase tracking-[0.2em] text-mute">{k}</p>
            <p className="mt-2 font-display text-4xl">{String(v)}</p>
          </Card>
        ))}
      </div>
      <Card className="mt-8">
        <h2 className="font-display text-2xl">Users</h2>
        <ul className="mt-4 space-y-2 text-sm">
          {(users.data || []).map((u) => (
            <li key={u.id}>
              {u.name} · {u.email} · {u.role}
            </li>
          ))}
        </ul>
        <p className="mt-4 text-sm text-mute">
          Create and edit job roles, resources, and roadmaps through the admin REST endpoints documented in README.md.
        </p>
      </Card>
    </div>
  );
}
