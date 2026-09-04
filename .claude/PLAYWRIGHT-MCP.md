# Playwright MCP server

Config lives in `.mcp.json` at the repo root. It points the server at the
Chromium already baked into the Claude Code web image rather than downloading
one.

## Status: configured, blocked on network policy

The config is correct but the server cannot run in the Claude Code **web**
environment as currently provisioned. Two independent blockers:

1. **The package cannot be downloaded.** `npm` returns HTTP 403 for every
   package, not just `@playwright/mcp` — `npm view lodash version` fails the
   same way. `npx -y @playwright/mcp@latest` therefore cannot start.
2. **The browser cannot reach the web.** Chromium launches and renders fine,
   but the egress gateway refuses outbound CONNECT:

   ```
   connect_rejected - gateway answered 403 to CONNECT (policy denial)
   host: example.com:443
   ```

Both are the environment's egress policy, chosen when the environment was
created. Neither is fixable from inside a session, and the agent-proxy docs
(`/root/.ccr/README.md`) say to report policy denials rather than route around
them.

## What works today

Local pages. The proxy bypass list includes `localhost`, `127.0.0.1` and
`file://` needs no network at all, so Playwright can screenshot anything this
container serves or generates. Verified working.

`scripts/shoot.js` does this without the MCP server — see below.

## To enable the MCP server

Open the environment's network egress policy to:

- `registry.npmjs.org` (so the package can install)
- whichever sites you need to browse

Network access is configured per environment, outside the session. See
https://code.claude.com/docs/en/claude-code-on-the-web

Once egress is open, the server starts automatically on the next session.
Claude Code will prompt once to approve a project-scoped MCP server.

Running Claude Code **locally** instead avoids all of this — your own machine
has normal network access, and `.mcp.json` works there as-is apart from
`--executable-path`, which should be dropped so Playwright uses its own
browser.

## Impact on the company-material-evaluation skill

That skill's third deliverable is a source screenshot folder — one image per
cited passage. It needs a browser that can load live source pages, so it
cannot be produced in the web environment while egress is closed. Search still
works; fetching and screenshotting specific pages does not.

## Unverified detail

The exact flag names above (`--isolated`, `--output-dir`, `--executable-path`)
are from prior knowledge of `@playwright/mcp`. They could not be checked
against the package, since npm and the docs site are both unreachable from
here. If the server errors on startup once egress opens, run
`npx @playwright/mcp@latest --help` and reconcile.
