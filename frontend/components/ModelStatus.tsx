'use client';
import { useEffect, useState } from 'react';
import { modelStatus } from '@/lib/api';
export default function ModelStatus() {
  const [status, setStatus] = useState<Record<
    string,
    { name: string; status: string; reason: string | null }
  > | null>(null);
  const [error, setError] = useState(false);
  useEffect(() => {
    let active = true;
    modelStatus()
      .then((s) => {
        if (active) setStatus(s);
      })
      .catch(() => {
        if (active) setError(true);
      });
    return () => {
      active = false;
    };
  }, []);
  if (error)
    return (
      <p className="muted">
        Live service status is unavailable. The model descriptions below remain available.
      </p>
    );
  if (!status) return <p role="status">Checking service configuration…</p>;
  return (
    <div className="completed" aria-label="Service configuration">
      {Object.entries(status).map(([task, state]) => (
        <span className="badge" key={task}>
          {state.name}: {state.status.replaceAll('_', ' ')}
        </span>
      ))}
    </div>
  );
}
