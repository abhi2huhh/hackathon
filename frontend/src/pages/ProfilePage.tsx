import { useAuth } from "../context/AuthContext";
import { Card } from "../components/ui/Card";

export default function ProfilePage() {
  const { user } = useAuth();
  return (
    <Card className="max-w-xl">
      <h1 className="font-display text-4xl">Profile</h1>
      <dl className="mt-6 space-y-3 text-sm">
        <div>
          <dt className="text-mute">Name</dt>
          <dd>{user?.name}</dd>
        </div>
        <div>
          <dt className="text-mute">Email</dt>
          <dd>{user?.email}</dd>
        </div>
        <div>
          <dt className="text-mute">Role</dt>
          <dd>{user?.role}</dd>
        </div>
      </dl>
    </Card>
  );
}
