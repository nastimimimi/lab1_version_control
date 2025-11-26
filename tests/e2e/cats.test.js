const { test, expect } = require('@playwright/test');

test('Показ випадкового котика', async ({ page }) => {
  await page.goto('/');
  const oldSrc = await page.locator('#catImg').getAttribute('src');
  await page.click('#randomBtn');
  const newSrc = await page.locator('#catImg').getAttribute('src');
  expect(oldSrc).not.toBe(newSrc);
});

test('Валідація полів форми', async ({ page }) => {
  await page.goto('/');
  await page.click('#sendBtn');
  const error = await page.evaluate(() => document.querySelector(':invalid'));
  expect(error).not.toBeNull();
});

test('Надсилання відгуку', async ({ page }) => {
  await page.goto('/');
  await page.fill('#username', 'KittyFan');
  await page.fill('#feedback', 'Найкращий котик!');
  await page.click('#sendBtn');
  await expect(page.locator('#message')).toBeVisible();
});
