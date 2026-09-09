'use client';
import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { capabilities, type Capabilities } from '@/lib/api';
type State = {
  status: 'checking' | 'online' | 'offline';
  data: Capabilities | null;
  refresh: () => void;
};
const ServiceContext = createContext<State>({ status: 'checking', data: null, refresh: () => {} });
export const useService = () => useContext(ServiceContext);
export function ServiceProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<Omit<State, 'refresh'>>({ status: 'checking', data: null });
  const refresh = useCallback(() => {
    capabilities()
      .then((data) => setState({ status: 'online', data }))
      .catch(() => setState({ status: 'offline', data: null }));
  }, []);
  useEffect(() => {
    let active = true;
    capabilities()
      .then((data) => {
        if (active) setState({ status: 'online', data });
      })
      .catch(() => {
        if (active) setState({ status: 'offline', data: null });
      });
    return () => {
      active = false;
    };
  }, []);
  return <ServiceContext value={{ ...state, refresh }}>{children}</ServiceContext>;
}
export function ServiceIndicator() {
  const { status, data, refresh } = useService();
  const label =
    status === 'checking'
      ? 'Connecting to service'
      : status === 'offline'
        ? 'Service unavailable'
        : data?.warming
          ? 'Models are warming up'
          : 'Analysis service connected';
  return (
    <button
      className={`service-indicator service-${status}`}
      type="button"
      onClick={refresh}
      title="Refresh connection status"
    >
      <span className="status-dot" />
      {label}
      <span aria-hidden="true">↻</span>
    </button>
  );
}
