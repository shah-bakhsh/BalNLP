import type { Metadata } from 'next';
import Link from 'next/link';
import { site, tasks } from '@/lib/config';
import Header from '@/components/Header';
import Logo from '@/components/Logo';
import { ServiceProvider } from '@/components/ServiceProvider';
import './globals.css';
export const metadata: Metadata = {
  title: { default: 'BalNLP — Open Balochi Natural Language Processing', template: '%s | BalNLP' },
  description:
    'Explore Balochi text with part-of-speech tagging, named entities, morphology, and dependency parsing.',
  openGraph: {
    title: 'BalNLP',
    description: 'Open Balochi Natural Language Processing',
    type: 'website',
  },
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <ServiceProvider>
          <a className="skip" href="#main">
            Skip to content
          </a>
          <Header />
          <main id="main">{children}</main>
          <footer className="site-footer">
            <div className="footer-main">
              <div className="footer-brand">
                <Link href="/" aria-label="BalNLP home">
                  <Logo />
                </Link>
                <p>
                  A closer look at Balochi language.
                  <br />
                  One word, one sentence, one connection at a time.
                </p>
              </div>
              <div>
                <h2>Explore</h2>
                <nav aria-label="Analysis tools">
                  {tasks.map((t) => (
                    <Link key={t.id} href={t.route}>
                      {t.name}
                    </Link>
                  ))}
                </nav>
              </div>
              <div>
                <h2>Resources</h2>
                <nav aria-label="Footer navigation">
                  <Link href="/models">The models</Link>
                  <Link href="/docs">Documentation</Link>
                  <a href={site.huggingface}>Hugging Face ↗</a>
                  {site.github && <a href={site.github}>GitHub ↗</a>}
                </nav>
              </div>
            </div>
            <div className="footer-bottom">
              <span>BalNLP · Supporting Balochi language technology.</span>
              <span>Research models. Please review predictions.</span>
            </div>
          </footer>
        </ServiceProvider>
      </body>
    </html>
  );
}
