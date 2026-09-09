'use client';
import { useState } from 'react';
import { tasks } from '@/lib/config';
import { copyText, download } from '@/lib/export';
import type { AnalysisResult, BalNLPToken } from '@/types/analysis';
import { DependencyTree } from './DependencyTree';

const display = (value: string | number | null | undefined) => value ?? '—';
const features = (token: BalNLPToken) =>
  token.feats === null
    ? '—'
    : Object.entries(token.feats)
        .map(([k, v]) => `${k}=${v}`)
        .join(' · ') || 'None';
export function TokenTable({ tokens }: { tokens: BalNLPToken[] }) {
  return (
    <div className="table-scroll" tabIndex={0} role="region" aria-label="Token details">
      <table>
        <caption className="sr-only">
          Word-level analysis. A dash means no prediction is available.
        </caption>
        <thead>
          <tr>
            {['ID', 'Word', 'Lemma', 'POS', 'NER', 'Morphology', 'Head', 'Relation'].map((h) => (
              <th key={h} scope="col">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tokens.map((t) => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td lang="bal" dir="rtl" className="word">
                {t.form}
              </td>
              <td lang="bal" dir="rtl">
                {display(t.lemma)}
              </td>
              <td>{display(t.upos)}</td>
              <td>{display(t.ner)}</td>
              <td>{features(t)}</td>
              <td>{display(t.head)}</td>
              <td>{display(t.deprel)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
function Export({ text, extension }: { text: string; extension: string }) {
  const [feedback, setFeedback] = useState('');
  return (
    <>
      <div className="export-actions">
        <button
          className="button secondary"
          onClick={async () => {
            try {
              await copyText(text);
              setFeedback('Copied to clipboard.');
            } catch {
              setFeedback('Copy failed. Please download the file instead.');
            }
          }}
        >
          Copy {extension === 'json' ? 'JSON' : 'CoNLL-U'}
        </button>
        <button className="button secondary" onClick={() => download(text, `balnlp.${extension}`)}>
          Download .{extension}
        </button>
        <span role="status">{feedback}</span>
      </div>
      <pre tabIndex={0}>{text}</pre>
    </>
  );
}
export default function Results({ result }: { result: AnalysisResult }) {
  const tabs = [
    'Overview',
    'Tokens',
    ...tasks.filter((t) => result.meta.completed_tasks.includes(t.id)).map((t) => t.short),
    'CoNLL-U',
    'JSON',
  ];
  const [tab, setTab] = useState('Overview');
  const active = tabs.includes(tab) ? tab : 'Overview';
  const chars = Array.from(result.text);
  const marked: React.ReactNode[] = [];
  let end = 0;
  result.entities.forEach((entity, index) => {
    marked.push(chars.slice(end, entity.start).join(''));
    marked.push(
      <mark key={index} className={`entity entity-${entity.label}`} title={entity.label}>
        {entity.text}
        <small>{entity.label}</small>
      </mark>,
    );
    end = entity.end;
  });
  marked.push(chars.slice(end).join(''));
  return (
    <section className="results" aria-label="Analysis results">
      <div className="results-heading">
        <div>
          <p className="eyebrow">YOUR ANALYSIS</p>
          <h2>A closer look at your text.</h2>
        </div>
        <span className="badge">
          {result.tokens.length} tokens · {(result.meta.total_ms / 1000).toFixed(1)}s
        </span>
      </div>
      {result.meta.failed_tasks.map((f) => (
        <div className="notice" key={f.task}>
          <strong>{tasks.find((t) => t.id === f.task)?.short} unavailable.</strong> {f.message}
        </div>
      ))}
      <div className="tabs" role="tablist" aria-label="Result views">
        {tabs.map((name, i) => (
          <button
            id={`tab-${name}`}
            key={name}
            role="tab"
            aria-selected={active === name}
            aria-controls="result-panel"
            tabIndex={active === name ? 0 : -1}
            onClick={() => setTab(name)}
            onKeyDown={(event) => {
              let next = i;
              if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
              else if (event.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
              else if (event.key === 'Home') next = 0;
              else if (event.key === 'End') next = tabs.length - 1;
              else return;
              event.preventDefault();
              setTab(tabs[next]);
              document.getElementById(`tab-${tabs[next]}`)?.focus();
            }}
          >
            {name}
          </button>
        ))}
      </div>
      <div
        id="result-panel"
        role="tabpanel"
        aria-labelledby={`tab-${active}`}
        tabIndex={0}
        className="result-panel"
      >
        {active === 'Overview' && (
          <>
            <div className="overview-text" dir="rtl" lang="bal">
              {result.text}
            </div>
            <div className="completed">
              {tasks
                .filter((t) => result.meta.completed_tasks.includes(t.id))
                .map((t) => (
                  <span className="badge" key={t.id}>
                    ✓ {t.short}
                  </span>
                ))}
            </div>
            <p className="muted">
              Select a view to explore predictions. A dash indicates an unavailable value.
            </p>
            <TokenTable tokens={result.tokens} />
          </>
        )}
        {active === 'Tokens' && <TokenTable tokens={result.tokens} />}
        {active === 'POS' && (
          <>
            <div className="token-chips" dir="rtl">
              {result.tokens.map((t) => (
                <div className={`token-chip pos-${t.upos}`} key={t.id}>
                  <span lang="bal">{t.form}</span>
                  <small>{display(t.upos)}</small>
                </div>
              ))}
            </div>
            <TokenTable tokens={result.tokens} />
          </>
        )}
        {active === 'Entities' && (
          <>
            <div className="overview-text entity-sentence" lang="bal" dir="rtl">
              {marked}
            </div>
            <div className="completed">
              {[...new Set(result.entities.map((e) => e.label))].map((label) => (
                <span className="badge" key={label}>
                  {label}
                </span>
              ))}
            </div>
            {result.entities.length ? (
              <ul className="entity-list">
                {result.entities.map((e, i) => (
                  <li key={i}>
                    <bdi lang="bal">{e.text}</bdi>
                    <span className="badge">{e.label}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No named entities were detected.</p>
            )}
          </>
        )}
        {active === 'Morphology' && (
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Word</th>
                  <th>Lemma</th>
                  <th>Features</th>
                </tr>
              </thead>
              <tbody>
                {result.tokens.map((t) => (
                  <tr key={t.id}>
                    <td dir="rtl" lang="bal">
                      {t.form}
                    </td>
                    <td dir="rtl" lang="bal">
                      {display(t.lemma)}
                    </td>
                    <td>{features(t)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {active === 'Dependencies' && (
          <>
            <DependencyTree tokens={result.tokens} />
            <TokenTable tokens={result.tokens} />
          </>
        )}
        {active === 'CoNLL-U' && <Export text={result.conllu} extension="conllu" />}
        {active === 'JSON' && <Export text={JSON.stringify(result, null, 2)} extension="json" />}
      </div>
    </section>
  );
}
