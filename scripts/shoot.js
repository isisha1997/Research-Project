#!/usr/bin/env node
// Screenshot a page with the Chromium already present in the Claude Code image.
//
// Works without the Playwright MCP server, which cannot install while npm is
// blocked by egress policy. See .claude/PLAYWRIGHT-MCP.md
//
//   node scripts/shoot.js <url> [output.png] [--full] [--width=1280] [--height=900]
//
// Remote URLs need open egress; file:// and localhost work today.

const path = require('path');

const PLAYWRIGHT = '/opt/node22/lib/node_modules/playwright';
const CHROMIUM = '/opt/pw-browsers/chromium';

const args = process.argv.slice(2);
const flags = new Map(
  args.filter(a => a.startsWith('--')).map(a => {
    const [k, v] = a.replace(/^--/, '').split('=');
    return [k, v === undefined ? true : v];
  })
);
const positional = args.filter(a => !a.startsWith('--'));

const url = positional[0];
if (!url) {
  console.error('usage: node scripts/shoot.js <url> [output.png] [--full]');
  process.exit(2);
}
const out = path.resolve(positional[1] || 'screenshot.png');

(async () => {
  const { chromium } = require(PLAYWRIGHT);
  const browser = await chromium.launch({
    headless: true,
    executablePath: CHROMIUM,
    args: ['--no-sandbox'],
  });
  try {
    const page = await browser.newPage({
      viewport: {
        width: Number(flags.get('width') || 1280),
        height: Number(flags.get('height') || 900),
      },
    });
    const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    await page.screenshot({ path: out, fullPage: Boolean(flags.get('full')) });
    console.log(`${resp ? resp.status() : '???'}  ${await page.title()}`);
    console.log(out);
  } finally {
    await browser.close();
  }
})().catch(err => {
  console.error(`failed: ${err.message}`);
  if (/ERR_TUNNEL_CONNECTION_FAILED|ERR_PROXY/.test(err.message)) {
    console.error('egress policy blocked this host - see .claude/PLAYWRIGHT-MCP.md');
  }
  process.exit(1);
});
