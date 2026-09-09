import { test, expect } from '@playwright/test';

test('real browser to FastAPI inference', async ({ page }) => {
  test.skip(
    process.env.BALNLP_LIVE_E2E !== '1',
    'Opt-in: requires backend on port 8000 with real cached models',
  );
  test.setTimeout(210000);
  await page.goto('/analyze');
  await page.getByRole('textbox', { name: /Your text/ }).fill('بلوچی متن');
  const responsePromise = page.waitForResponse((r) => r.url().endsWith('/api/v1/analyze'), {
    timeout: 195000,
  });
  await page.getByRole('button', { name: 'Analyze Text' }).click();
  const response = await responsePromise;
  expect(response.status()).toBe(200);
  const result = await response.json();
  expect(result.meta.completed_tasks).toEqual(['pos', 'ner', 'morph', 'parser']);
  expect(result.meta.failed_tasks.map((f: { task: string }) => f.task)).toEqual([]);
  await expect(page.getByRole('tab', { name: 'Dependencies', exact: true })).toBeVisible();
  await page.getByRole('tab', { name: 'Dependencies', exact: true }).click();
  await expect(page.getByRole('img', { name: /Dependency tree/ })).toBeVisible();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: '../docs/screenshots/analysis-real-models.png', fullPage: true });
});
