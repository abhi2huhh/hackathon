import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";

export default function NotFoundPage() {
  return (
    <div className="py-24 text-center">
      <h1 className="font-display text-6xl">Lost in the stacks</h1>
      <p className="mt-3 text-mute">That route is not part of the atelier.</p>
      <Link to="/">
        <Button className="mt-6">Return home</Button>
      </Link>
    </div>
  );
}
