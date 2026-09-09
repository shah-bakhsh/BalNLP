import Link from 'next/link';
export const metadata = { title: 'Documentation' };
export default function Page() {
  return (
    <article className="shell prose">
      <p className="eyebrow">GETTING STARTED</p>
      <h1>From text to understanding.</h1>
      <p>
        BalNLP brings Balochi language models into one workspace. Enter Arabic-script text and
        choose the analysis you need.
      </p>
      <h2>Analyze a sentence</h2>
      <ol>
        <li>
          Open the <Link href="/analyze">analysis workspace</Link>.
        </li>
        <li>Type or paste a Balochi sentence.</li>
        <li>Choose Complete Analysis or an individual task, then select Analyze Text.</li>
        <li>Explore the results and download JSON or CoNLL-U.</li>
      </ol>
      <h2>Reading your results</h2>
      <p>
        POS identifies grammatical roles. Entities highlights recognized names. Morphology describes
        lemmas and word features when available. Dependencies shows connections between words, with
        HEAD 0 representing the sentence root.
      </p>
      <p>
        A dash means a value is unavailable. If a model fails, successful analyses remain visible,
        with an explanation of the missing result.
      </p>
      <h2>Long sentences and first requests</h2>
      <p>
        The service loads models when needed, so the first request may take longer. If a sentence
        exceeds a model’s input limit, split it into shorter sentences. Please retry later if the
        service is busy.
      </p>
      <h2>API quick start</h2>
      <pre>{`POST /api/v1/analyze\nContent-Type: application/json\n\n{"text":"بلوچی متن","tasks":["pos","ner","parser"]}`}</pre>
      <p>
        Individual endpoints: <code>/api/v1/pos</code>, <code>/api/v1/ner</code>,{' '}
        <code>/api/v1/morph</code>, and <code>/api/v1/parse</code>. The backend serves interactive
        API documentation at <code>/api/docs</code> in the combined deployment.
      </p>
      <h2>Export conventions</h2>
      <p>
        JSON token IDs are document-wide. Dependency HEAD values refer to those IDs, with 0 for
        ROOT. CoNLL-U restarts IDs at each sentence. Character offsets refer to the NFC-normalized
        response text and count Unicode code points.
      </p>
      <h2>Privacy and limitations</h2>
      <p>
        BalNLP does not persist submitted text or analysis history, and it does not log your
        sentence. Text is transmitted to the configured analysis backend and held temporarily in
        memory. Research predictions may be incorrect; review results before relying on them.
      </p>
      <p>
        BalMorph uses the recovered v2 inference definition. All four analyses use the published
        models. An unknown lemma rule produces no lemma rather than a guessed value. You can check
        availability on the <Link href="/models">Models page</Link>.
      </p>
    </article>
  );
}
