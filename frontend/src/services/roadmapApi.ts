import { api } from "./api";

export const roadmapApi = {
  list: () => api<any[]>("/roadmaps"),
  detail: (id: number) => api<any>(`/roadmaps/${id}`),
  progress: (id: number, body: { step_id: number; completed: boolean }) =>
    api<any>(`/roadmaps/${id}/progress`, { method: "POST", body: JSON.stringify(body) }),
};
