'use client';
import Link from 'next/link';
import { useEffect, useRef, useState } from 'react';
import { analyze } from '@/lib/api';
import { examples } from '@/lib/examples';
import { site, tasks } from '@/lib/config';
import type { AnalysisResult, Selection } from '@/types/analysis';
import Results from './Results';
import TaskIcon from './TaskIcon';
import { useService, ServiceIndicator } from './ServiceProvider';

export default function AnalysisWorkspace({ initialTask = 'all' }: { initialTask?: Selection }) {
  const [text, setText] = useState(''),
    [selection, setSelection] = useState<Selection>(initialTask);
  const [result, setResult] = useState<AnalysisResult | null>(null),
    [error, setError] = useState('');
  const [loading, setLoading] = useState(false),
    [cold, setCold] = useState(false),
    [invalid, setInvalid] = useState(false);
  const request = useRef<AbortController | null>(null),
    form = useRef<HTMLFormElement | null>(null),
    results = useRef<HTMLDivElement | null>(null);
  const service = useService();
  const limit = service.data?.max_text_length || site.maxLength;
  useEffect(() => () => request.current?.abort(), []);
  const count = Array.from(text).length;
  const current = tasks.find((t) => t.id === initialTask);
  const unavailable = service.data ? tasks.filter((t) => !service.data!.tasks[t.id].enabled) : [];
  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (loading) return;
    if (!text.trim()) {
      setInvalid(true);
      setError('Please enter Balochi text.');
      document.getElementById('balochi-text')?.focus();
      return;
    }
    if (count > limit) {
      setInvalid(true);
      setError(`Please use at most ${limit} characters.`);
      return;
    }
    setError('');
    setInvalid(false);
    setResult(null);
    setLoading(true);
    setCold(false);
    const controller = new AbortController();
    request.current = controller;
    const timer = setTimeout(() => setCold(true), 12000);
    try {
      setResult(await analyze(text, selection, controller.signal));
      requestAnimationFrame(() => results.current?.focus());
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Analysis failed. Please try again.');
    } finally {
      clearTimeout(timer);
      setLoading(false);
      setCold(false);
    }
  }
  return (
    <div className="shell workspace">
      <div className="workspace-breadcrumb">
        <Link href="/">Home</Link>
        <span>/</span>
        <span>{current?.short || 'Workspace'}</span>
      </div>
      <div className="workspace-title-row">
        <div className="page-heading">
          <p className="eyebrow">YOUR BALOCHI LANGUAGE WORKSPACE</p>
          <h1>{current?.name || 'Explore your Balochi text.'}</h1>
          <p>
            {current?.description ||
              'Understand the words, discover the names, and explore the structure.'}
          </p>
        </div>
        <ServiceIndicator />
      </div>
      <form ref={form} onSubmit={submit} noValidate className="workspace-grid">
        <div className="editor-column">
          <section className="input-card">
            <div className="input-heading">
              <label htmlFor="balochi-text">
                <span className="step-number">01</span>Your text{' '}
                <span className="muted">/ بلوچی</span>
              </label>
              <button
                type="button"
                className="text-link"
                disabled={loading}
                onClick={() => {
                  setText(examples[0].text);
                  setError('');
                  setInvalid(false);
                  setResult(null);
                }}
              >
                Use example ↙
              </button>
            </div>
            <textarea
              id="balochi-text"
              aria-describedby="input-help text-count"
              aria-invalid={invalid}
              lang="bal"
              dir="rtl"
              placeholder="بلوچی متن"
              value={text}
              readOnly={loading}
              onKeyDown={(e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                  e.preventDefault();
                  form.current?.requestSubmit();
                }
              }}
              onChange={(e) => {
                setText(e.target.value);
                setResult(null);
                setError('');
                setInvalid(false);
              }}
              rows={4}
            />
            <div className="input-meta">
              <p id="input-help">
                Arabic-script Balochi · Keep sentences short for faster results.
              </p>
              <span id="text-count" className={count > limit ? 'invalid' : ''}>
                {count.toLocaleString()} / {limit.toLocaleString()}
              </span>
            </div>
            <div className="editor-toolbar">
              <span className="keyboard-hint">
                <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to analyze
              </span>
              <button
                type="button"
                className="text-link"
                disabled={loading || !text}
                onClick={() => {
                  setText('');
                  setResult(null);
                  setError('');
                  setInvalid(false);
                }}
              >
                Clear text
              </button>
            </div>
          </section>
          <div className="privacy-panel">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              aria-hidden="true"
            >
              <path d="m12 3 8 3v6c0 4-5 8-8 9-3-1-8-5-8-9V6l8-3Z" />
              <path d="m8 12 3 3 5-6" />
            </svg>
            <div>
              <strong>Your words stay yours.</strong>
              <p>
                Text is processed for this request. BalNLP does not save your text or analysis
                history.
              </p>
            </div>
          </div>
          {unavailable.length > 0 && (
            <div className="availability-note">
              <strong>{unavailable.map((t) => t.short).join(', ')} is not connected yet.</strong>
              <span>
                Complete Analysis returns the connected models.{' '}
                <Link href="/models">Model details →</Link>
              </span>
            </div>
          )}
        </div>
        <aside className="task-panel">
          <div className="task-panel-title">
            <span className="step-number">02</span>
            <h2>Choose your analysis</h2>
          </div>
          <fieldset className="task-options" disabled={loading}>
            <legend className="sr-only">Analysis</legend>
            {[
              {
                id: 'all' as Selection,
                name: 'Complete Analysis',
                description: 'Run the full language toolkit.',
              },
              ...tasks,
            ].map((t) => (
              <label
                className={`task-option ${selection === t.id ? 'task-selected' : ''}`}
                key={t.id}
              >
                <input
                  type="radio"
                  name="analysis-task"
                  value={t.id}
                  checked={selection === t.id}
                  onChange={() => setSelection(t.id)}
                />
                <span className="task-option-icon">
                  <TaskIcon task={t.id} />
                </span>
                <span>
                  <b>{t.name}</b>
                  <small>
                    {t.id === 'all' ? 'All connected models, one result.' : t.description}
                  </small>
                </span>
                <span className="radio-circle" />
              </label>
            ))}
          </fieldset>
          <button className="button primary analyze-button" disabled={loading} type="submit">
            {loading ? 'Analyzing…' : 'Analyze Text'}
            <span aria-hidden="true">→</span>
          </button>
          <p className="task-note">Research predictions · Review before use</p>
        </aside>
      </form>
      {error && (
        <div className="error" role="alert">
          <strong>Analysis could not finish.</strong>
          <p>{error}</p>
          <span>Your text is still above. You can edit it and try again.</span>
        </div>
      )}
      {loading && (
        <div className="loading-panel" role="status" aria-live="polite">
          <span className="spinner" />
          <div>
            <h2>Analyzing Balochi text…</h2>
            <p>
              {cold
                ? 'The service is loading its models. Your first request may take longer.'
                : 'Your selected models are processing the sentence.'}
            </p>
          </div>
        </div>
      )}
      <div ref={results} tabIndex={-1} className="results-anchor">
        {result && <Results key={result.meta.total_ms + result.text} result={result} />}
      </div>
      {!result && !loading && !error && (
        <div className="empty workspace-empty">
          <div className="empty-icon">
            <TaskIcon task={initialTask} />
          </div>
          <div>
            <p className="eyebrow">READY WHEN YOU ARE</p>
            <h2>Your results will appear here.</h2>
            <p>Start with a sentence above. Then explore predictions and export your results.</p>
          </div>
          <div className="empty-formats">
            <span>JSON</span>
            <span>CoNLL-U</span>
          </div>
        </div>
      )}
    </div>
  );
}
