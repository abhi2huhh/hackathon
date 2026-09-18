const BASE = import.meta.env.VITE_API_URL || "/api";

export class ApiRequestError extends Error {
  status: number;
  code: string;
  constructor(message: string, status: number, code: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

function token() {
  return localStorage.getItem("access_token");
}

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (!(init.body instanceof FormData) && !headers.has("Content-Type") && init.body) {
    headers.set("Content-Type", "application/json");
  }
  const jwt = token();
  if (jwt) headers.set("Authorization", `Bearer ${jwt}`);
  const response = await fetch(`${BASE}${path}`, { ...init, headers });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload.success === false) {
    const message = payload?.error?.message || "The server could not complete this request.";
    const code = payload?.error?.code || "REQUEST_FAILED";
    if (response.status === 401 && !path.startsWith("/auth/login")) {
      localStorage.removeItem("access_token");
    }
    throw new ApiRequestError(message, response.status, code);
  }
  return payload.data as T;
}

export const apiRaw = api;
