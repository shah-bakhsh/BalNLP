export const site = {
  name: 'BalNLP',
  version: '0.1.0',
  github: process.env.NEXT_PUBLIC_GITHUB_URL || 'https://github.com/shah-bakhsh/BalNLP',
  huggingface: 'https://huggingface.co/shah-bakhsh',
  maxLength: Number(process.env.NEXT_PUBLIC_MAX_TEXT_LENGTH) || 2000,
};
export const tasks = [
  {
    id: 'pos',
    name: 'POS Tagging',
    short: 'POS',
    route: '/pos',
    description: 'Understand the role of every word: nouns, verbs, adjectives, and more.',
    symbol: 'Aa',
  },
  {
    id: 'ner',
    name: 'Named Entity Recognition',
    short: 'Entities',
    route: '/ner',
    description: 'Find the people, places, organizations, and times mentioned in your text.',
    symbol: '◌',
  },
  {
    id: 'morph',
    name: 'Morphological Analysis',
    short: 'Morphology',
    route: '/morphology',
    description: 'Explore word forms, lemmas, and grammatical features.',
    symbol: '⌘',
  },
  {
    id: 'parser',
    name: 'Dependency Parsing',
    short: 'Dependencies',
    route: '/parser',
    description: 'See how words connect to form the structure of a sentence.',
    symbol: '↳',
  },
] as const;
