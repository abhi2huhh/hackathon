export function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full border border-line px-3 py-1 text-[11px] uppercase tracking-[0.18em] text-mute">
      {children}
    </span>
  );
}
