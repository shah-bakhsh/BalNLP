import type { Selection } from '@/types/analysis';
export default function TaskIcon({ task }: { task: Selection }) {
  const paths = {
    all: (
      <>
        <rect x="4" y="4" width="6" height="6" rx="1.5" />
        <rect x="14" y="4" width="6" height="6" rx="1.5" />
        <rect x="4" y="14" width="6" height="6" rx="1.5" />
        <rect x="14" y="14" width="6" height="6" rx="1.5" />
      </>
    ),
    pos: (
      <>
        <path d="m4 19 6-14 6 14M6.5 14h7M17 11h4m-2-2v10" />
      </>
    ),
    ner: (
      <>
        <path d="M8 4H4v4m12-4h4v4M4 16v4h4m12-4v4h-4" />
        <circle cx="12" cy="10" r="2.5" />
        <path d="M7.5 17a4.5 4.5 0 0 1 9 0" />
      </>
    ),
    morph: (
      <>
        <path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5M3 16l9 5 9-5" />
      </>
    ),
    parser: (
      <>
        <rect x="9" y="3" width="6" height="5" rx="1" />
        <rect x="2" y="16" width="6" height="5" rx="1" />
        <rect x="16" y="16" width="6" height="5" rx="1" />
        <path d="M12 8v4m-7 4v-4h14v4" />
      </>
    ),
  };
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[task]}
    </svg>
  );
}
