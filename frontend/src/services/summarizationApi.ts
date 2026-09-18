import { api } from "./api";

export const summarizationApi = {
  text: (body: { text: string; line_count: number; method: string; title?: string }) =>
    api<any>("/summarization", { method: "POST", body: JSON.stringify(body) }),
  document: (form: FormData) =>
    api<any>("/summarization/document", { method: "POST", body: form }),
};
