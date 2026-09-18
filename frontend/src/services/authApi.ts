import { api } from "./api";
import type { User } from "../types";

export const authApi = {
  register: (body: { name: string; email: string; password: string }) =>
    api<{ user: User; access_token: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  login: (body: { email: string; password: string }) =>
    api<{ user: User; access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  me: () => api<User>("/auth/me"),
  logout: () => api("/auth/logout", { method: "POST" }),
};
