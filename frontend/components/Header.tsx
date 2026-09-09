'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import Logo from './Logo';
export default function Header() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const links = [
    ['/analyze', 'Workspace'],
    ['/models', 'Models'],
    ['/docs', 'Documentation'],
    ['/about', 'About'],
  ];
  return (
    <header className="header">
      <div className="header-inner">
        <Link href="/" aria-label="BalNLP home" onClick={() => setOpen(false)}>
          <Logo />
        </Link>
        <button
          className="menu-toggle"
          aria-label={open ? 'Close navigation' : 'Open navigation'}
          aria-expanded={open}
          aria-controls="main-navigation"
          onClick={() => setOpen(!open)}
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            aria-hidden="true"
          >
            <path d={open ? 'm6 6 12 12M18 6 6 18' : 'M4 6h16M4 12h16M4 18h16'} />
          </svg>
        </button>
        <nav id="main-navigation" className={open ? 'nav-open' : ''} aria-label="Main navigation">
          {links.map(([href, label]) => (
            <Link
              href={href}
              key={href}
              aria-current={path === href ? 'page' : undefined}
              onClick={() => setOpen(false)}
            >
              {label}
            </Link>
          ))}
        </nav>
        <Link className="header-cta" href="/analyze">
          Analyze text <span>↗</span>
        </Link>
      </div>
    </header>
  );
}
