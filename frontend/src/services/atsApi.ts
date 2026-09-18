import { api } from "./api";

export const atsApi = {
  roles: () => api<any[]>("/ats/roles"),
  analyze: (form: FormData) =>
    api<any>("/ats/analyze", { method: "POST", body: form }),
  history: () => api<any[]>("/ats/history"),
};
