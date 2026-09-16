# Agent Customization Repository

## Canonical Sources

This repository is the source of truth for the personal agent customizations used by the local VS Code and Copilot installations.

- VS Code user instructions and agents belong under `vscode/user/prompts/`.
- Copilot skills belong under `copilot/skills/<skill-name>/`.
- Keep each customization's filename and frontmatter compatible with the host that discovers it.

## Editing Rules

- Edit canonical files in this repository, not files reached through the linked user paths.
- Preserve valid YAML frontmatter and meaningful `name` and `description` values.
- Keep always-on instructions concise because they are loaded broadly.
- Do not add credentials, tokens, private keys, or machine-specific secrets.
- When adding a customization, update `README.md` if its discovery path or setup instructions change.

## Repository-Owned Fiji Customizations

Any Fiji-specific agent and skill are maintained by the `fiji-llm` repository and
are intentionally not duplicated here:

- `fiji-llm/doc/agents/vscode/fiji-mcp.agent.md`
- `fiji-llm/doc/agents/vscode/fiji-script-debugging/SKILL.md`

## Link Validation

Prefer links when the checkout is actively being developed so changes are picked
up immediately. Native symbolic links require Windows Developer Mode or
administrator privileges; copying is the portable fallback.

The managed discovery path on Windows is:

- `%APPDATA%\\Code\\User\\prompts`
- `%USERPROFILE%\\.copilot\\skills\\fiji-script-debugging`

Use `Get-Item` to confirm that the path is a junction or symbolic link, and
verify that the expected files resolve through it. Directory junctions are the
supported no-admin fallback used by this installation.
