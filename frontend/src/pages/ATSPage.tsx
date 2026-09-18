import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { motion } from "motion/react";
import { atsApi } from "../services/atsApi";
import { Button } from "../components/ui/Button";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function ATSPage() {
  const roles = useQuery({ queryKey: ["roles"], queryFn: atsApi.roles });
  const [roleId, setRoleId] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [stage, setStage] = useState("");
  const mutation = useMutation({
    mutationFn: async () => {
      if (!file || !roleId) throw new Error("Select a job role and upload a PDF or DOCX resume.");
      setStage("Uploading document");
      const form = new FormData();
      form.append("job_role_id", roleId);
      form.append("file", file);
      setStage("Extracting content");
      const result = await atsApi.analyze(form);
      setStage("Analyzing");
      return result;
    },
  });
  const result = mutation.data;

  return (
    <div>
      <h1 className="font-display text-5xl">Resume compatibility atelier</h1>
      <p className="mt-3 max-w-2xl text-mute">
        Estimated compatibility with a selected role — skill match, keywords, and semantic overlap. This is not an
        employer ATS score.
      </p>
      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <section className="rounded-3xl border border-line bg-panel p-6">
          <h2 className="font-display text-2xl">Upload</h2>
          <label className="mt-4 block text-sm">
            Job role
            <select
              className="mt-2 w-full rounded-2xl border border-line bg-ink px-3 py-3"
              value={roleId}
              onChange={(e) => setRoleId(e.target.value)}
            >
              <option value="">Select</option>
              {(roles.data || []).map((role: any) => (
                <option key={role.id} value={role.id}>
                  {role.title}
                </option>
              ))}
            </select>
          </label>
          <label className="mt-4 block text-sm">
            Resume (PDF or DOCX)
            <input
              className="mt-2 block w-full text-sm"
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>
          <Button className="mt-6 w-full" disabled={mutation.isPending} onClick={() => mutation.mutate()}>
            {mutation.isPending ? stage || "Working…" : "Analyze"}
          </Button>
        </section>
        <section className="rounded-3xl border border-line bg-panel p-6">
          <h2 className="font-display text-2xl">Progress</h2>
          <p className="mt-4 text-mute">{mutation.isPending ? stage : "Idle until you run an analysis."}</p>
          {mutation.isError && <div className="mt-4"><ErrorNote message={(mutation.error as Error).message} /></div>}
        </section>
        <section className="rounded-3xl border border-line bg-panel p-6">
          <h2 className="font-display text-2xl">Result</h2>
          {!result && <p className="mt-4 text-mute">The circular score will appear here.</p>}
          {result && (
            <div>
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="mx-auto mt-4 grid h-36 w-36 place-items-center rounded-full border-4 border-accent font-display text-4xl text-accent"
              >
                {Math.round(result.score)}
              </motion.div>
              <p className="mt-3 text-center text-xs text-mute">{result.disclaimer}</p>
              <p className="mt-4 text-sm">Matched: {(result.matched_skills || []).join(", ") || "—"}</p>
              <p className="mt-2 text-sm">Missing: {(result.missing_skills || []).join(", ") || "—"}</p>
              <ul className="mt-3 list-disc pl-5 text-sm text-mute">
                {(result.suggestions || []).map((s: string) => (
                  <li key={s}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
