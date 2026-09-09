import ModelStatus from '@/components/ModelStatus';
export const metadata = { title: 'Models' };
const models = [
  {
    name: 'BalBERT',
    repo: 'BalBERT',
    task: 'Language backbone',
    text: 'Balochi-adapted XLM-RoBERTa representations underpin the task-specific models.',
    status: 'Backbone',
    metrics: '',
  },
  {
    name: 'BalPOS',
    repo: 'BalPOS',
    task: 'Part-of-speech tagging',
    text: 'Assigns a Universal POS tag to each word using a fine-tuned token classifier.',
    status: 'Integrated',
    metrics: '',
  },
  {
    name: 'BalNER v2',
    repo: 'BalNER-v2',
    task: 'Named entity recognition',
    text: 'Recognizes people, locations, organizations, and time expressions with BIO labels.',
    status: 'Integrated',
    metrics: '',
  },
  {
    name: 'BalMorph v2',
    repo: 'BalMorph',
    task: 'Morphology and lemmas',
    text: 'Predicts lemmas and grammatical features using the verified BalMorph v2 notebook architecture and learned edit rules.',
    status: 'Integrated',
    metrics: '',
  },
  {
    name: 'BalParser v2',
    repo: 'BalParser',
    task: 'Dependency parsing',
    text: 'Combines a fine-tuned BalBERT encoder with a biaffine parser and single-root tree decoding.',
    status: 'Integrated',
    metrics:
      'Author-reported locked test set: Macro F1 46.78%, Weighted F1 71.13%, Root Accuracy 64.71%.',
  },
];
export default function Page() {
  return (
    <div className="shell prose">
      <p className="eyebrow">THE MODELS BEHIND THE WORDS</p>
      <h1>A connected Balochi toolkit.</h1>
      <p>
        Each model brings a different perspective to your text. These are research models, and their
        predictions may contain errors.
      </p>
      <ModelStatus />
      <div className="model-grid">
        {models.map((m) => (
          <article className="model-card" key={m.name}>
            <span className="badge">{m.status}</span>
            <h2>{m.name}</h2>
            <p className="eyebrow">{m.task}</p>
            <p>{m.text}</p>
            {m.name === 'BalParser v2' && (
              <div className="metric">
                <span>
                  <b>54.33%</b>UAS
                </span>
                <span>
                  <b>45.23%</b>LAS
                </span>
              </div>
            )}
            {m.metrics && <p>{m.metrics}</p>}
            <a href={`https://huggingface.co/shah-bakhsh/${m.repo}`}>View on Hugging Face ↗</a>
          </article>
        ))}
      </div>
      <p>
        “Configured” describes service settings; it does not guarantee that a checkpoint has loaded
        successfully.
      </p>
    </div>
  );
}
