import { api } from "./api";

export const resourceApi = {
  list: (params: Record<string, string | number | undefined>) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== "") query.set(k, String(v));
    });
    const suffix = query.toString() ? `?${query}` : "";
    return api<any>(`/resources${suffix}`);
  },
  detail: (id: number) => api<any>(`/resources/${id}`),
  bookmark: (id: number) => api<any>(`/resources/${id}/bookmark`, { method: "POST" }),
  bookmarks: () => api<any[]>("/resources/bookmarks"),
};
