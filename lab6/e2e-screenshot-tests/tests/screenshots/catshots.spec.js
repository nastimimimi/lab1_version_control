const { test, expect } = require('@playwright/test');

test('Скріншот всієї сторінки', async ({ page }) => {
  await page.goto('/');
  expect(await page.screenshot()).toMatchSnapshot('full-page.png');
});

test('Скрін заголовка', async ({ page }) => {
  await page.goto('/');
  const h1 = page.locator('h1');
  expect(await h1.screenshot()).toMatchSnapshot('title.png');
});
