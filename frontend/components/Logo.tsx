export function LogoMark({ className = '' }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <rect width="48" height="48" rx="13" fill="currentColor" />
      <path
        d="M15 12v24m0-23h12a6 6 0 0 1 0 12H15m0 0h14a5.5 5.5 0 0 1 0 11H15"
        stroke="white"
        strokeWidth="2.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="15" cy="13" r="3.5" fill="#abe5c6" />
      <circle cx="15" cy="25" r="3.5" fill="#abe5c6" />
      <circle cx="15" cy="36" r="3.5" fill="#abe5c6" />
    </svg>
  );
}
export default function Logo() {
  return (
    <span className="logo">
      <LogoMark className="logo-mark" />
      <span className="logo-type">
        Bal<span>NLP</span>
        <small>BALOCHI LANGUAGE LAB</small>
      </span>
    </span>
  );
}
