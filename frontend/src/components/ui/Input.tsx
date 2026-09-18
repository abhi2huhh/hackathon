import { forwardRef } from "react";
import { cn } from "../../lib/utils";

export const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  function Input({ className, ...props }, ref) {
    return (
      <input
        ref={ref}
        className={cn(
          "w-full rounded-2xl border border-line bg-ink/60 px-4 py-3 text-paper placeholder:text-mute/70",
          className,
        )}
        {...props}
      />
    );
  },
);

