import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import { useAuth } from "../context/AuthContext";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Skeleton } from "../components/loaders/Skeleton";
import { ErrorNote } from "../components/ui/ErrorNote";

const actions = [
  { to: "/ats", label: "Analyze resume" },
  { to: "/summarizer", label: "Summarize text" },
  { to: "/rag", label: "Ask a document" },
  { to: "/roadmaps", label: "Explore roadmaps" },
  { to: "/resources", label: "Find resources" },
  { to: "/search", label: "Search the atelier" },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const query = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => api<any>("/users/me/dashboard"),
  });

  if (query.isLoading) return <Skeleton className="h-64" />;
  if (query.isError) return <ErrorNote message={(query.error as Error).message} />;
  const data = query.data;

  return (
    <div>
      <p className="text-xs uppercase tracking-[0.28em] text-bronze">Studio desk</p>
      <h1 className="mt-2 font-display text-5xl">Good to see you, {user?.name.split(" ")[0]}.</h1>
      <div className="mt-6 flex flex-wrap gap-2">
        {actions.map((a) => (
          <Link key={a.to} to={a.to}>
            <Button variant="line">{a.label}</Button>
          </Link>
        ))}
      </div>
      <div className="mt-10 grid gap-5 md:grid-cols-2">
        <Card>
          <h2 className="font-display text-2xl">ATS analyses</h2>
          <ul className="mt-4 space-y-2 text-sm text-mute">
            {(data.ats_analyses || []).length === 0 && <li>No analyses yet.</li>}
            {(data.ats_analyses || []).map((item: any) => (
              <li key={item.id}>
                Score {item.score} — {item.role?.title || "role"}
              </li>
            ))}
          </ul>
        </Card>
        <Card>
          <h2 className="font-display text-2xl">Roadmap progress</h2>
          <ul className="mt-4 space-y-2 text-sm text-mute">
            {(data.roadmap_progress || []).length === 0 && <li>Start a roadmap to track steps here.</li>}
            {(data.roadmap_progress || []).map((item: any) => (
              <li key={item.roadmap.id}>
                {item.roadmap.title}: {item.percent}%
              </li>
            ))}
          </ul>
        </Card>
        <Card>
          <h2 className="font-display text-2xl">Documents</h2>
          <ul className="mt-4 space-y-2 text-sm text-mute">
            {(data.documents || []).length === 0 && <li>Upload a PDF or DOCX in RAG.</li>}
            {(data.documents || []).map((item: any) => (
              <li key={item.id}>{item.title}</li>
            ))}
          </ul>
        </Card>
        <Card>
          <h2 className="font-display text-2xl">Activity</h2>
          <ul className="mt-4 space-y-2 text-sm text-mute">
            {(data.activity || []).length === 0 && <li>Your actions will appear here.</li>}
            {(data.activity || []).map((item: any) => (
              <li key={item.id}>
                {item.action}
                {item.detail ? ` · ${item.detail}` : ""}
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
}
