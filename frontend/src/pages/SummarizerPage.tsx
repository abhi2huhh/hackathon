import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { summarizationApi } from "../services/summarizationApi";
import { Button } from "../components/ui/Button";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function SummarizerPage() {
  const [text, setText] = useState("");
  const [lineCount, setLineCount] = useState(5);
  const [method, setMethod] = useState("extractive");
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({
    mutationFn: async () => {
      if (file) {
        const form = new FormData();
        form.append("file", file);
        form.append("line_count", String(lineCount));
        form.append("method", method);
        return summarizationApi.document(form);
      }
      return summarizationApi.text({ text, line_count: lineCount, method });
    },
  });

  return (
    <div>
      <h1 className="font-display text-5xl">Compression desk</h1>
      <p className="mt-3 text-mute">Extractive TF-IDF is always available. Abstractive requires a configured LLM key.</p>
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <section className="rounded-3xl border border-line bg-panel p-6">
          <textarea
            className="min-h-[280px] w-full rounded-2xl border border-line bg-ink p-4"
            placeholder="Paste research, notes, or a lecture transcript…"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <input className="mt-3 text-sm" type="file" accept=".pdf,.docx,.txt" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <div className="mt-4 flex flex-wrap gap-2">
            {[3, 5, 10, 15].map((n) => (
              <Button key={n} variant={lineCount === n ? "primary" : "line"} onClick={() => setLineCount(n)}>
                {n} lines
              </Button>
            ))}
            <label className="flex items-center gap-2 text-sm">
              Custom
              <input
                type="number"
                min={3}
                max={20}
                className="w-16 rounded-lg border border-line bg-ink px-2 py-1"
                value={lineCount}
                onChange={(e) => setLineCount(Number(e.target.value))}
              />
            </label>
          </div>
          <div className="mt-3 flex gap-2">
            {["extractive", "abstractive"].map((m) => (
              <Button key={m} variant={method === m ? "primary" : "line"} onClick={() => setMethod(m)}>
                {m}
              </Button>
            ))}
          </div>
          <Button className="mt-5" disabled={mutation.isPending} onClick={() => mutation.mutate()}>
            {mutation.isPending ? "Compressing…" : "Generate summary"}
          </Button>
          <p className="mt-2 text-xs text-mute">{text.length} characters</p>
        </section>
        <section className="rounded-3xl border border-line bg-panel p-6">
          {mutation.isError && <ErrorNote message={(mutation.error as Error).message} />}
          {mutation.data && (
            <div>
              <div className="flex gap-2">
                <Button
                  variant="line"
                  onClick={() => navigator.clipboard.writeText(mutation.data.summary)}
                >
                  Copy
                </Button>
                <Button
                  variant="line"
                  onClick={() => {
                    const blob = new Blob([mutation.data.summary], { type: "text/plain" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "summary.txt";
                    a.click();
                  }}
                >
                  Download
                </Button>
                <Button variant="ghost" onClick={() => mutation.mutate()}>
                  Regenerate
                </Button>
              </div>
              <p className="mt-4 whitespace-pre-wrap leading-7">{mutation.data.summary}</p>
              <p className="mt-4 text-xs text-mute">
                {mutation.data.method} · {mutation.data.summary_length} / {mutation.data.original_length} chars
              </p>
            </div>
          )}
          {!mutation.data && !mutation.isError && <p className="text-mute">The distilled text appears on this side.</p>}
        </section>
      </div>
    </div>
  );
}
