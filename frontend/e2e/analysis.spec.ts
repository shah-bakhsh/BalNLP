import { test, expect } from '@playwright/test';
test('analyze text, render RTL results, export, and remain within viewport', async ({
  page,
}, info) => {
  await page.route('**/api/v1/analyze', async (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        text: 'بلوچی متن',
        language: 'bal',
        tokens: [
          {
            id: 1,
            form: 'بلوچی',
            start: 0,
            end: 5,
            sentence_id: 1,
            lemma: null,
            upos: 'NOUN',
            ner: 'O',
            feats: null,
            head: 2,
            deprel: 'nsubj',
          },
          {
            id: 2,
            form: 'متن',
            start: 6,
            end: 9,
            sentence_id: 1,
            lemma: null,
            upos: 'VERB',
            ner: 'O',
            feats: null,
            head: 0,
            deprel: 'root',
          },
        ],
        entities: [],
        dependency_tree: {},
        conllu: '1\tبلوچی\t_\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\tمتن\t_\tVERB\t_\t_\t0\troot\t_\t_\n',
        meta: {
          completed_tasks: ['pos', 'ner', 'parser'],
          failed_tasks: [
            {
              task: 'morph',
              code: 'MODEL_NOT_AVAILABLE',
              message: 'Morphology is awaiting its inference definition.',
            },
          ],
          warnings: [],
          total_ms: 120,
        },
      }),
    }),
  );
  await page.goto('/analyze');
  await expect(page.getByRole('textbox', { name: /Your text/ })).toHaveAttribute('dir', 'rtl');
  await page.getByRole('textbox', { name: /Your text/ }).fill('بلوچی متن');
  await page.getByRole('button', { name: 'Analyze Text' }).click();
  await expect(page.getByRole('tab', { name: 'POS', exact: true })).toBeVisible();
  await expect(page.getByText('Morphology unavailable.')).toBeVisible();
  await page.getByRole('tab', { name: 'Dependencies', exact: true }).click();
  await expect(page.getByRole('img', { name: /Dependency tree/ })).toBeVisible();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: `../docs/screenshots/analysis-${info.project.name}.png`,
    fullPage: true,
  });
  await page.getByRole('tab', { name: 'JSON', exact: true }).click();
  const downloadEvent = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download .json' }).click();
  expect((await downloadEvent).suggestedFilename()).toBe('balnlp.json');
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth,
  );
  expect(overflow).toBe(false);
});
test('home and routes render without page errors', async ({ page }, info) => {
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(error.message));
  for (const route of [
    '/',
    '/pos',
    '/ner',
    '/morphology',
    '/parser',
    '/models',
    '/docs',
    '/about',
  ]) {
    await page.goto(route);
    await expect(page.locator('h1')).toBeVisible();
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth),
    ).toBe(false);
  }
  await page.goto('/');
  if (info.project.name === 'mobile') {
    await page.getByRole('button', { name: 'Open navigation' }).click();
    await expect(page.getByRole('navigation', { name: 'Main navigation' })).toBeVisible();
    await page.getByRole('button', { name: 'Close navigation' }).click();
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: `../docs/screenshots/home-${info.project.name}.png`,
    fullPage: true,
  });
  expect(errors).toEqual([]);
});
