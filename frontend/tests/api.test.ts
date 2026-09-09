import { afterEach, expect, it, vi } from 'vitest';
import { analyze } from '@/lib/api';
afterEach(() => vi.unstubAllGlobals());
it('uses the parse endpoint and preserves the server error', async () => {
  const fetch = vi
    .fn()
    .mockResolvedValue({
      ok: false,
      status: 503,
      json: async () => ({ error: { message: 'Model unavailable.' } }),
    });
  vi.stubGlobal('fetch', fetch);
  await expect(analyze('بلوچی', 'parser')).rejects.toThrow('Model unavailable.');
  expect(fetch.mock.calls[0][0]).toMatch(/\/parse$/);
});
it('handles non-JSON unavailable responses', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: false,
      status: 502,
      json: async () => {
        throw new Error();
      },
    }),
  );
  await expect(analyze('بلوچی', 'pos')).rejects.toThrow('unavailable');
});
