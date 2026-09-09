import Link from 'next/link';
export default function NotFound() {
  return (
    <div className="shell prose">
      <h1>Page not found.</h1>
      <p>
        Return to the <Link href="/analyze">analysis workspace</Link> to continue.
      </p>
    </div>
  );
}
