import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export function Protected({ children, admin = false }: { children: React.ReactNode; admin?: boolean }) {
  const { user, loading } = useAuth();
  if (loading) return <p className="text-mute">Checking your session…</p>;
  if (!user) return <Navigate to="/login" replace />;
  if (admin && user.role !== "ADMIN") return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}
