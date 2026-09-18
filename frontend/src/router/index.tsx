import { createBrowserRouter } from "react-router-dom";
import { lazy, Suspense, type ReactElement } from "react";
import { AppShell } from "../components/layout/AppShell";
import { Protected } from "../components/navigation/Protected";

const LandingPage = lazy(() => import("../pages/LandingPage"));
const LoginPage = lazy(() => import("../pages/LoginPage"));
const RegisterPage = lazy(() => import("../pages/RegisterPage"));
const DashboardPage = lazy(() => import("../pages/DashboardPage"));
const ATSPage = lazy(() => import("../pages/ATSPage"));
const SummarizerPage = lazy(() => import("../pages/SummarizerPage"));
const RAGPage = lazy(() => import("../pages/RAGPage"));
const RoadmapsPage = lazy(() => import("../pages/RoadmapsPage"));
const RoadmapDetailPage = lazy(() => import("../pages/RoadmapDetailPage"));
const ResourcesPage = lazy(() => import("../pages/ResourcesPage"));
const ResourceDetailPage = lazy(() => import("../pages/ResourceDetailPage"));
const SearchPage = lazy(() => import("../pages/SearchPage"));
const ProfilePage = lazy(() => import("../pages/ProfilePage"));
const AdminPage = lazy(() => import("../pages/AdminPage"));
const NotFoundPage = lazy(() => import("../pages/NotFoundPage"));

function wrap(el: ReactElement, auth = false, admin = false) {
  const inner = <Suspense fallback={<p className="text-mute">Loading…</p>}>{el}</Suspense>;
  if (!auth) return inner;
  return <Protected admin={admin}>{inner}</Protected>;
}

export const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { path: "/", element: wrap(<LandingPage />) },
      { path: "/login", element: wrap(<LoginPage />) },
      { path: "/register", element: wrap(<RegisterPage />) },
      { path: "/dashboard", element: wrap(<DashboardPage />, true) },
      { path: "/ats", element: wrap(<ATSPage />, true) },
      { path: "/summarizer", element: wrap(<SummarizerPage />, true) },
      { path: "/rag", element: wrap(<RAGPage />, true) },
      { path: "/roadmaps", element: wrap(<RoadmapsPage />, true) },
      { path: "/roadmaps/:id", element: wrap(<RoadmapDetailPage />, true) },
      { path: "/resources", element: wrap(<ResourcesPage />, true) },
      { path: "/resources/:id", element: wrap(<ResourceDetailPage />, true) },
      { path: "/search", element: wrap(<SearchPage />, true) },
      { path: "/profile", element: wrap(<ProfilePage />, true) },
      { path: "/admin", element: wrap(<AdminPage />, true, true) },
      { path: "*", element: wrap(<NotFoundPage />) },
    ],
  },
]);
