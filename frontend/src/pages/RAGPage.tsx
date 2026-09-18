import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { ragApi } from "../services/ragApi";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { ErrorNote } from "../components/ui/ErrorNote";

export default function RAGPage() {
  const qc = useQueryClient();
  const docs = useQuery({ queryKey: ["docs"], queryFn: ragApi.documents });
  const [selected, setSelected] = useState<number | null>(null);
  const [question, setQuestion] = useState("What methodology was used?");
  const [stage, setStage] = useState("");
  const upload = useMutation({
    mutationFn: async (file: File) => {
      setStage("Uploading document");
      const form = new FormData();
      form.append("file", file);
      form.append("title", file.name);
      setStage("Extracting content");
      const doc = await ragApi.upload(form);
      setStage("Indexing passages");
      return doc;
    },
    onSuccess: (doc) => {
      qc.invalidateQueries({ queryKey: ["docs"] });
      setSelected(doc.id);
      setStage("");
    },
  });
  const ask = useMutation({
    mutationFn: async () => {
      if (!selected) throw new Error("Select or upload a document first.");
      setStage("Retrieving relevant context");
      const result = await ragApi.query({ document_id: selected, question });
      setStage("Generating response");
      return result;
    },
  });
  const current = (docs.data || []).find((d: any) => d.id === selected);

  return (
    <div>
      <h1 className="font-display text-5xl">Document intelligence</h1>
      <p className="mt-3 text-mute">Answers are grounded in retrieved passages. Missing LLM keys still return sources.</p>
      <div className="mt-8 grid gap-5 lg:grid-cols-3">
        <section className="rounded-3xl border border-line bg-panel p-5">
          <h2 className="font-display text-2xl">Library</h2>
          <input
            className="mt-4 text-sm"
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => e.target.files?.[0] && upload.mutate(e.target.files[0])}
          />
          <ul className="mt-4 space-y-2">
            {(docs.data || []).map((doc: any) => (
              <li key={doc.id}>
                <button
                  className={`w-full rounded-2xl px-3 py-2 text-left text-sm ${selected === doc.id ? "bg-accent text-ink" : "bg-ink"}`}
                  onClick={() => setSelected(doc.id)}
                >
                  {doc.title}
                </button>
              </li>
            ))}
          </ul>
          {upload.isError && <div className="mt-3"><ErrorNote message={(upload.error as Error).message} /></div>}
        </section>
        <section className="rounded-3xl border border-line bg-panel p-5">
          <h2 className="font-display text-2xl">Document</h2>
          {current ? (
            <dl className="mt-4 space-y-2 text-sm text-mute">
              <div>Type: {current.file_type}</div>
              <div>Characters: {current.char_count}</div>
              <div>Chunks: {current.chunk_count}</div>
            </dl>
          ) : (
            <p className="mt-4 text-mute">Select a file to inspect its index.</p>
          )}
          <p className="mt-6 text-xs uppercase tracking-[0.2em] text-bronze">{stage}</p>
        </section>
        <section className="rounded-3xl border border-line bg-panel p-5">
          <h2 className="font-display text-2xl">Ask</h2>
          <Input className="mt-4" value={question} onChange={(e) => setQuestion(e.target.value)} />
          <Button className="mt-3" disabled={ask.isPending} onClick={() => ask.mutate()}>
            {ask.isPending ? "Retrieving…" : "Ask from context"}
          </Button>
          {ask.isError && <div className="mt-3"><ErrorNote message={(ask.error as Error).message} /></div>}
          {ask.data && (
            <div className="mt-5 space-y-4 text-sm">
              <p>{ask.data.answer || ask.data.message}</p>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-bronze">Sources</p>
                {(ask.data.retrieved_chunks || []).map((c: any) => (
                  <blockquote key={c.chunk_index} className="mt-2 border-l border-accent pl-3 text-mute">
                    {c.text.slice(0, 280)}
                  </blockquote>
                ))}
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
