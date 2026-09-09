import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import AnalysisWorkspace from '@/components/AnalysisWorkspace';
import { analyze } from '@/lib/api';
vi.mock('@/lib/api', () => ({ analyze: vi.fn() }));
const fixture = {
  text: 'بلوچی متن',
  language: 'bal',
  tokens: [
    {
      id: 1,
      form: 'بلوچی',
      start: 0,
      end: 5,
      sentence_id: 1,
      upos: 'NOUN',
      ner: null,
      lemma: null,
      feats: null,
      head: null,
      deprel: null,
    },
  ],
  entities: [],
  dependency_tree: {},
  conllu: '1\tبلوچی\t_\tNOUN\t_\t_\t_\t_\t_\t_\n',
  meta: { completed_tasks: ['pos'] as 'pos'[], failed_tasks: [], warnings: [], total_ms: 20 },
};
describe('analysis workspace', () => {
  it('rejects blank input without contacting the API', () => {
    render(<AnalysisWorkspace />);
    fireEvent.click(screen.getByRole('button', { name: 'Analyze Text' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Please enter Balochi text');
    expect(analyze).not.toHaveBeenCalled();
  });
  it('renders a response and only relevant result tabs', async () => {
    vi.mocked(analyze).mockResolvedValueOnce(fixture);
    render(<AnalysisWorkspace />);
    fireEvent.click(screen.getByRole('button', { name: /Use example/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Analyze Text' }));
    await screen.findByRole('tab', { name: 'POS' });
    expect(screen.queryByRole('tab', { name: 'Morphology' })).toBeNull();
    fireEvent.click(screen.getByRole('tab', { name: 'JSON' }));
    expect(screen.getByRole('tabpanel')).toHaveTextContent('NOUN');
  });
  it('shows loading then a friendly service error', async () => {
    let reject!: (e: Error) => void;
    vi.mocked(analyze).mockImplementationOnce(
      () =>
        new Promise((_, rej) => {
          reject = rej;
        }),
    );
    render(<AnalysisWorkspace />);
    fireEvent.click(screen.getByRole('button', { name: /Use example/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Analyze Text' }));
    expect(screen.getByRole('status')).toHaveTextContent('Analyzing Balochi');
    reject(new Error('The model could not load.'));
    await waitFor(() =>
      expect(screen.getByRole('alert')).toHaveTextContent('The model could not load.'),
    );
  });
});
