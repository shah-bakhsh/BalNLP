import Link from 'next/link';
import { tasks } from '@/lib/config';
import TaskIcon from '@/components/TaskIcon';

export default function Home() {
  return (
    <>
      <section className="hero shell">
        <div className="hero-copy">
          <p className="eyebrow">
            <span className="dot" /> A LANGUAGE. A WORLD OF POSSIBILITIES.
          </p>
          <h1>
            Open Balochi
            <br />
            <em>Natural Language</em>
            <br />
            Processing.
          </h1>
          <p className="hero-description">
            From individual words to the structure of a sentence. Explore Balochi with one unified
            language toolkit.
          </p>
          <div className="actions">
            <Link className="button primary" href="/analyze">
              Analyze Balochi Text <span>↗</span>
            </Link>
            <Link className="text-link" href="/models">
              Explore Models <span>→</span>
            </Link>
          </div>
          <p className="hero-note">
            No account needed <span>·</span> Arabic-script support <span>·</span> Open research
          </p>
        </div>
        <div className="language-panel" aria-label="Balochi language toolkit">
          <div className="panel-top">
            <span>BALOCHI / بلوچی</span>
            <span>
              LANGUAGE LAB <span className="dot" />
            </span>
          </div>
          <div className="balochi-word" lang="bal" dir="rtl">
            بلوچی
          </div>
          <p className="panel-caption">A closer look at language.</p>
          <div className="flow">
            <span>Text</span>
            <i>→</i>
            <span>Words</span>
            <i>→</i>
            <span>Structure</span>
          </div>
          <div className="panel-bottom">
            <span>BalBERT-powered models</span>
            <span>01 — 04</span>
          </div>
        </div>
      </section>
      <section className="tool-section shell">
        <div className="section-title">
          <div>
            <p className="eyebrow">ONE PLATFORM, FOUR PERSPECTIVES</p>
            <h2>Make sense of every sentence.</h2>
          </div>
          <Link className="text-link" href="/analyze">
            Open the workspace →
          </Link>
        </div>
        <div className="feature-grid">
          {tasks.map((task, i) => (
            <Link className="feature" key={task.id} href={task.route}>
              <div className="feature-top">
                <span className="feature-icon">
                  <TaskIcon task={task.id} />
                </span>
                <span className="muted">0{i + 1}</span>
              </div>
              <h3>{task.name}</h3>
              <p>{task.description}</p>
              <span className="feature-bottom">
                Explore {task.short.toLowerCase()} <b>↗</b>
              </span>
            </Link>
          ))}
        </div>
      </section>
      <section className="research-strip shell">
        <span className="eyebrow">BUILT FOR EXPLORATION</span>
        <h2>
          Balochi words.
          <br />
          More ways to understand them.
        </h2>
        <div>
          <p>
            Inspect predictions, explore sentence structure, and take your results with you in JSON
            or CoNLL-U.
          </p>
          <Link className="text-link" href="/docs">
            Read the documentation →
          </Link>
        </div>
      </section>
    </>
  );
}
