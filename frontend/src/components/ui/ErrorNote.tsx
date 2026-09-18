export function ErrorNote({ message }: { message: string }) {
  return (
    <div role="alert" className="rounded-2xl border border-danger/40 bg-danger/10 px-4 py-3 text-sm text-paper">
      {message}
    </div>
  );
}
