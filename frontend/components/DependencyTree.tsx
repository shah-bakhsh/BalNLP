import type { BalNLPToken } from '@/types/analysis';

export function DependencyTree({ tokens }: { tokens: BalNLPToken[] }) {
  const sentences = [...new Set(tokens.map((t) => t.sentence_id))];
  return (
    <div>
      {sentences.map((sid) => {
        const words = tokens.filter((t) => t.sentence_id === sid);
        if (
          words.some(
            (t) => t.head === null || (t.head !== 0 && !words.some((w) => w.id === t.head)),
          )
        )
          return <p key={sid}>The tree could not be displayed. Use the token table below.</p>;
        const width = Math.max(600, (words.length + 1) * 112),
          height = 110 + Math.min(words.length, 12) * 22;
        const baseline = height - 48;
        const x = (id: number) => (id === 0 ? 45 : 145 + words.findIndex((t) => t.id === id) * 112);
        return (
          <div className="tree-scroll" key={sid}>
            <svg
              width={width}
              height={height}
              role="img"
              aria-label={`Dependency tree for sentence ${sid}. Details are available in the token table.`}
            >
              <defs>
                <marker
                  id={`arrow-${sid}`}
                  markerWidth="6"
                  markerHeight="6"
                  refX="5"
                  refY="3"
                  orient="auto"
                >
                  <path d="M0,0 L6,3 L0,6" fill="currentColor" />
                </marker>
              </defs>
              <text x="45" y={baseline + 26} textAnchor="middle" className="tree-root">
                ROOT
              </text>
              {words.map((t) => {
                const from = x(t.head!),
                  to = x(t.id),
                  arc = baseline - 30 - Math.min(Math.abs(to - from) / 112, 12) * 19;
                return (
                  <g key={t.id}>
                    <path
                      d={`M${from},${baseline} C${from},${arc} ${to},${arc} ${to},${baseline}`}
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.3"
                      markerEnd={`url(#arrow-${sid})`}
                    />
                    <text
                      x={(from + to) / 2}
                      y={(baseline + 3 * arc) / 4 - 5}
                      textAnchor="middle"
                      className="tree-label"
                    >
                      {t.deprel}
                    </text>
                    <text x={to} y={baseline + 26} textAnchor="middle" lang="bal" direction="rtl">
                      {t.form}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
        );
      })}
    </div>
  );
}
