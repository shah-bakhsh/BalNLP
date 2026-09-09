'use client';
export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <div className="shell prose">
      <h1>This page could not load.</h1>
      <p>Please try again.</p>
      <button className="button primary" onClick={reset}>
        Try again
      </button>
    </div>
  );
}
