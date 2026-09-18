import { Link, NavLink, useNavigate } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { useAuth } from "../../context/AuthContext";
import { Button } from "../ui/Button";

const links = [
  { to: "/", label: "Home" },
  { to: "/ats", label: "ATS" },
  { to: "/summarizer", label: "Summarizer" },
  { to: "/rag", label: "RAG" },
  { to: "/roadmaps", label: "Roadmaps" },
  { to: "/resources", label: "Resources" },
];

export function Navbar() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 border-b border-line/80 bg-ink/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
        <Link to="/" className="font-display text-xl tracking-tight">
          InnoLearn
        </Link>
        <nav className="hidden items-center gap-6 lg:flex" aria-label="Primary">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `text-sm ${isActive ? "text-accent" : "text-mute hover:text-paper"}`
              }
            >
              {link.label}
            </NavLink>
          ))}
          {user && (
            <>
              <NavLink to="/dashboard" className="text-sm text-mute hover:text-paper">
                Dashboard
              </NavLink>
              <NavLink to="/profile" className="text-sm text-mute hover:text-paper">
                Profile
              </NavLink>
              {user.role === "ADMIN" && (
                <NavLink to="/admin" className="text-sm text-mute hover:text-paper">
                  Admin
                </NavLink>
              )}
            </>
          )}
        </nav>
        <div className="hidden items-center gap-3 lg:flex">
          {user ? (
            <Button variant="line" onClick={() => { logout(); navigate("/"); }}>
              Sign out
            </Button>
          ) : (
            <>
              <Button variant="ghost" onClick={() => navigate("/login")}>
                Sign in
              </Button>
              <Button onClick={() => navigate("/register")}>Create account</Button>
            </>
          )}
        </div>
        <button
          className="lg:hidden"
          aria-label={open ? "Close menu" : "Open menu"}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border-t border-line lg:hidden"
          >
            <div className="flex flex-col gap-3 px-5 py-5">
              {links.map((link) => (
                <NavLink key={link.to} to={link.to} onClick={() => setOpen(false)} className="py-1 text-lg">
                  {link.label}
                </NavLink>
              ))}
              {user ? (
                <Button
                  variant="line"
                  onClick={() => {
                    logout();
                    setOpen(false);
                    navigate("/");
                  }}
                >
                  Sign out
                </Button>
              ) : (
                <Button onClick={() => { setOpen(false); navigate("/login"); }}>Sign in</Button>
              )}
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
