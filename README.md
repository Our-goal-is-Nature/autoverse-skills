# Autoverse Skills

Official Agent Skills for the Autoverse scholarly literature CLI.

## Install

Install all Skills globally:

```bash
npx skills add Our-goal-is-Nature/autoverse-skills -g -y
```

Install one Skill:

```bash
npx skills add Our-goal-is-Nature/autoverse-skills --skill autoverse-cli -g -y
npx skills add Our-goal-is-Nature/autoverse-skills --skill autoverse-topic-prep -g -y
npx skills add Our-goal-is-Nature/autoverse-skills --skill autoverse-seed-expand -g -y
npx skills add Our-goal-is-Nature/autoverse-skills --skill universe-research -g -y
```

Update the installed Skills:

```bash
npx skills update autoverse-cli autoverse-topic-prep autoverse-seed-expand universe-research -g -y
```

The [`skills`](https://github.com/vercel-labs/skills) CLI supports Codex, Claude Code, Cursor, Antigravity, and other compatible Agents.

## Included Skills

| Skill | Use it for |
|---|---|
| `autoverse-cli` | Install, authenticate, call, or troubleshoot the Autoverse CLI itself |
| `autoverse-topic-prep` | Explore a broad research direction when no seed paper is available |
| `autoverse-seed-expand` | Expand from a specific paper or author into references, citations, related work, or that author's other publications |
| `universe-research` | Write a computer science, medicine, or engineering literature review and evidence table |

Install the execution surface separately:

```bash
pipx install autoverse
autoverse login
```

There is no MCP product path. Agents use the CLI's `--json --quiet` contract.

## Versions

The current Skill Pack version and supported CLI range are in [`manifest.json`](./manifest.json). Each `SKILL.md` also carries its own `metadata.version`.

- Skill Pack: `0.4.3`
- Compatible CLI: `>=0.3.0,<0.4.0`

CLI and Skills are versioned independently. Upgrade them with `pipx upgrade autoverse` and `npx skills update ...` respectively.

## Source and validation

The maintained source lives in the private Autoverse CLI repository and is mirrored here for public distribution. CI validates:

- manifest, folder, name, and version agreement;
- referenced local files;
- official `npx skills` discovery and isolated installation.

Review Skills before using them; installed Skills run with the permissions of the selected Agent.

## License

Apache License 2.0. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
