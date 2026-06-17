# Day 4 — AI Vibe Coding with Claude Code

Turn the Day-3 pipeline into an AI-driven workflow. You install Claude Code, connect a few tools (MCP servers), and define reusable `/workflows` that crawl, build, query, and report — then run them step by step. "Vibe coding": you describe each step in plain language and the AI does the work.

## This repo
Starts (almost) empty on purpose — **you build the project here with Claude Code.** Your `/workflow` command files live in `.claude/commands/` as you create them, and the pipeline's outputs (data, schema, app) land in this repo. Push it to GitHub at the end (Section 4.3).

## Submit
Push this repo to GitHub: your `.claude/commands/` workflow files + the pipeline you built (crawl → schema → app → report).

---

## The lab, section by section

### Section 1 — Install Claude Code
Install Claude Code (`brew install --cask claude-code` / PowerShell installer), then `claude`. Learn the basic commands (`/help`, `claude mcp …`, `/mcp`).

### Section 2 — Connect Tools with MCP
What you do **not** need MCP for (Claude Code already edits files + runs `git`/`python`/`sqlite3`). Add servers with `claude mcp add` — the easy uvx/npx ones (`fetch`, `fs`, `git`), the **GitHub MCP** (a CLI-binary server, needs a token), and the kinds of MCP server (on-demand / CLI-binary / remote). Test with a git round-trip (`gh` CLI).

### Section 3 — Define Your Workflows
Make a `/workflow` (a command file in `.claude/commands/`). Build the **four workflows** that are the Day-3 pipeline: `/crawl` → `schedule.csv` · `/build` → load into SQLite · `/query` → extract · `/report` → write it up.

### Section 4 — Validate & Report
`/validate` (check it's all correct) · `/report` (write the report) · **4.3 Submit** — push your project to GitHub with the git MCP and hand in the link.
