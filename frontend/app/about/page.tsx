import { site } from '@/lib/config';
export const metadata = { title: 'About' };
export default function Page() {
  return (
    <article className="shell prose">
      <p className="eyebrow">LANGUAGE TECHNOLOGY FOR BALOCHI</p>
      <h1>More tools for a living language.</h1>
      <p>
        BalNLP unifies the BalBERT, BalPOS, BalNER, BalMorph, and BalParser model family in an
        accessible interface and a reusable Python library.
      </p>
      <h2>Built for exploration</h2>
      <p>
        The platform supports language researchers, students, and developers exploring Balochi text.
        It makes model outputs easier to inspect, compare, and export.
      </p>
      <h2>Research, with its limitations visible</h2>
      <p>
        These models are trained on limited data. Their behavior across Balochi varieties and
        unfamiliar domains has not been established. BalNLP presents predictions as model outputs
        and leaves unavailable fields empty.
      </p>
      <p>
        Model development: Shah Bakhsh. Find the published checkpoints on{' '}
        <a href={site.huggingface}>Hugging Face</a>.
      </p>
      <h2>A focused first release</h2>
      <p>
        No accounts, no database, and no saved text history. BalNLP loads models on demand and
        processes them sequentially by default.
      </p>
    </article>
  );
}
