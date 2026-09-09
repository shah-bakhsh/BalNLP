export type Task = 'pos' | 'ner' | 'morph' | 'parser';
export type Selection = 'all' | Task;
export interface BalNLPToken {
  id: number;
  form: string;
  start: number;
  end: number;
  sentence_id: number;
  lemma: string | null;
  upos: string | null;
  ner: string | null;
  feats: Record<string, string> | null;
  head: number | null;
  deprel: string | null;
}
export interface Entity {
  text: string;
  label: string;
  start: number;
  end: number;
  token_ids: number[];
}
export interface AnalysisResult {
  text: string;
  language: string;
  tokens: BalNLPToken[];
  entities: Entity[];
  dependency_tree: {
    edges?: { head: number; dependent: number; relation: string; sentence_id: number }[];
  };
  conllu: string;
  meta: {
    completed_tasks: Task[];
    failed_tasks: { task: Task; code: string; message: string }[];
    total_ms: number;
    warnings: string[];
  };
}
