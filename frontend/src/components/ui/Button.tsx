import { cn } from "../../lib/utils";

export function Button({
  className,
  variant = "primary",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost" | "line";
}) {
  const styles = {
    primary: "bg-accent text-ink hover:brightness-110",
    ghost: "bg-transparent text-paper hover:bg-white/5",
    line: "border border-line text-paper hover:border-accent/60",
  };
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5 text-sm font-medium transition duration-300 disabled:opacity-50",
        styles[variant],
        className,
      )}
      {...props}
    />
  );
}
