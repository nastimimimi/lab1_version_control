import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'tests',
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    trace: 'on-first-retry'
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] }},
    { name: 'firefox', use: { ...devices['Desktop Firefox'] }},
    { name: 'mobile', use: { ...devices['iPhone 12'] }}
  ],

  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  }
});
