import type { AnalysisResult, Selection, Task } from '@/types/analysis';
const base = (process.env.NEXT_PUBLIC_API_URL || '/api/v1').replace(/\/$/, '');
export interface Capabilities {
  max_text_length: number;
  max_tokens: number;
  warming: boolean;
  tasks: Record<Task, { enabled: boolean; status: string; loaded: boolean }>;
}
export async function capabilities(): Promise<Capabilities> {
  const response = await fetch(`${base}/capabilities`, {
    signal: AbortSignal.timeout(15000),
    cache: 'no-store',
  });
  if (!response.ok) throw new Error('Service unavailable');
  return response.json();
}
export async function analyze(
  text: string,
  selection: Selection,
  signal?: AbortSignal,
): Promise<AnalysisResult> {
  const controller = new AbortController();
  const abort = () => controller.abort();
  signal?.addEventListener('abort', abort, { once: true });
  if (signal?.aborted) controller.abort();
  const timeout = setTimeout(abort, 195000);
  try {
    const endpoint = selection === 'all' ? 'analyze' : selection === 'parser' ? 'parse' : selection;
    const response = await fetch(`${base}/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
      signal: controller.signal,
      cache: 'no-store',
    });
    const data = await response.json().catch(() => null);
    if (!response.ok)
      throw new Error(
        data?.error?.message ||
          (response.status === 429
            ? 'Too many requests. Please wait a minute.'
            : 'The analysis service is unavailable. Please try again shortly.'),
      );
    if (!data || !Array.isArray(data.tokens) || !data.meta || typeof data.conllu !== 'string')
      throw new Error('The service returned an unreadable response. Please try again.');
    return data;
  } catch (error) {
    if (controller.signal.aborted)
      throw new Error(
        'Analysis timed out or was cancelled. The service may still be starting. Please try again shortly.',
      );
    if (error instanceof TypeError)
      throw new Error(
        'Could not reach the analysis service. Please check your connection and try again.',
      );
    throw error;
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener('abort', abort);
  }
}
export async function modelStatus(): Promise<
  Record<string, { name: string; status: string; reason: string | null }>
> {
  const response = await fetch(`${base}/models`, {
    signal: AbortSignal.timeout(15000),
    cache: 'no-store',
  });
  if (!response.ok) throw new Error('Status unavailable');
  return response.json();
}
