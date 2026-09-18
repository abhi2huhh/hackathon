export function EmptyState({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-3xl border border-dashed border-line px-6 py-12 text-center">
      <h3 className="font-display text-2xl">{title}</h3>
      <p className="mt-2 text-sm text-mute">{body}</p>
    </div>
  );
}
