import { api } from "./api";

export const ragApi = {
  documents: () => api<any[]>("/rag/documents"),
  upload: (form: FormData) => api<any>("/rag/upload", { method: "POST", body: form }),
  query: (body: { document_id: number; question: string }) =>
    api<any>("/rag/query", { method: "POST", body: JSON.stringify(body) }),
};
