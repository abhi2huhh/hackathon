import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { ErrorNote } from "../components/ui/ErrorNote";
import { ApiRequestError } from "../services/api";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [show, setShow] = useState(false);
  const form = useForm({ resolver: zodResolver(schema) });

  return (
    <div className="mx-auto grid max-w-4xl gap-10 md:grid-cols-2">
      <div>
        <p className="text-xs uppercase tracking-[0.28em] text-bronze">Return to the atelier</p>
        <h1 className="mt-3 font-display text-5xl">Sign in</h1>
        <p className="mt-3 text-mute">Your analyses, documents, and progress stay on this account.</p>
      </div>
      <form
        className="space-y-4 rounded-[2rem] border border-line bg-panel p-8"
        onSubmit={form.handleSubmit(async (values) => {
          setError("");
          try {
            await login(values.email, values.password);
            navigate("/dashboard");
          } catch (err) {
            setError(err instanceof ApiRequestError ? err.message : "Unable to sign in.");
          }
        })}
      >
        {error && <ErrorNote message={error} />}
        <label className="block text-sm">
          Email
          <Input type="email" className="mt-2" {...form.register("email")} />
        </label>
        <label className="block text-sm">
          Password
          <div className="relative">
            <Input type={show ? "text" : "password"} className="mt-2 pr-24" {...form.register("password")} />
            <button type="button" className="absolute right-3 top-5 text-xs text-mute" onClick={() => setShow((v) => !v)}>
              {show ? "Hide" : "Show"}
            </button>
          </div>
        </label>
        <Button disabled={form.formState.isSubmitting} className="w-full">
          {form.formState.isSubmitting ? "Signing in…" : "Enter"}
        </Button>
        <p className="text-sm text-mute">
          New here? <Link className="text-accent" to="/register">Create an account</Link>
        </p>
      </form>
    </div>
  );
}
