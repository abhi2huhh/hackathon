export type User = {
  id: number;
  name: string;
  email: string;
  role: "USER" | "ADMIN";
  created_at?: string;
};

export type ApiError = {
  success: false;
  error: { code: string; message: string; details?: unknown };
};

export type ApiSuccess<T> = {
  success: true;
  data: T;
  message: string;
};
