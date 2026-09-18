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
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
});

export default function RegisterPage() {
  const { register: signup } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const form = useForm({ resolver: zodResolver(schema) });

  return (
    <div className="mx-auto grid max-w-4xl gap-10 md:grid-cols-2">
      <div>
        <p className="text-xs uppercase tracking-[0.28em] text-bronze">Join the atelier</p>
        <h1 className="mt-3 font-display text-5xl">Create your desk</h1>
        <p className="mt-3 text-mute">Registration stores a hashed password. We never keep plaintext credentials.</p>
      </div>
      <form
        className="space-y-4 rounded-[2rem] border border-line bg-panel p-8"
        onSubmit={form.handleSubmit(async (values) => {
          setError("");
          try {
            await signup(values.name, values.email, values.password);
            navigate("/dashboard");
          } catch (err) {
            setError(err instanceof ApiRequestError ? err.message : "Unable to create this account.");
          }
        })}
      >
        {error && <ErrorNote message={error} />}
        <label className="block text-sm">
          Name
          <Input className="mt-2" {...form.register("name")} />
        </label>
        <label className="block text-sm">
          Email
          <Input type="email" className="mt-2" {...form.register("email")} />
        </label>
        <label className="block text-sm">
          Password
          <Input type="password" className="mt-2" {...form.register("password")} />
        </label>
        <Button disabled={form.formState.isSubmitting} className="w-full">
          {form.formState.isSubmitting ? "Creating…" : "Create account"}
        </Button>
        <p className="text-sm text-mute">
          Already enrolled? <Link className="text-accent" to="/login">Sign in</Link>
        </p>
      </form>
    </div>
  );
}
