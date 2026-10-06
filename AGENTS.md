# Agent Customization Repository

## Canonical Sources

This repository is the source of truth for the personal agent customizations used by the local VS Code and Copilot installations.

- Copilot user agents belong under `vscode/user/agents/`.
- Copilot user instructions belong under `vscode/user/instructions/`.
- VS Code user MCP configuration and launcher sources belong under
	`vscode/user/mcp/`.
- Keep each customization's filename and frontmatter compatible with the host that discovers it.

## Editing Rules

- Edit canonical files in this repository, not files reached through the linked user paths.
- Preserve valid YAML frontmatter and meaningful `name` and `description` values.
- Keep always-on instructions concise because they are loaded broadly.
- Do not add credentials, tokens, private keys, or machine-specific secrets.
- When adding a customization, update `README.md` if its discovery path or setup instructions change.

## Serena Source Lookup

Keep `fiji-llm` active during normal work. Use Serena's `query_project` from
that active project to inspect local dependency checkouts; do not switch the
active project just to read source. The MCP server should use
`--add-mode query-projects` and `--project <fiji-llm-path>`.

When a checkout needs to be added to Serena's project list, use this temporary
setup procedure:

1. Change the Serena MCP command to `--context agent`, then restart the MCP
	server.
2. Call `activate_project` once for each absolute checkout root. Use the
	repository or Maven module root, not `src`, `target`, or a parent directory
	that only aggregates modules. No onboarding is needed for source lookup.
3. Activate `fiji-llm` again.
4. Stop the Serena MCP server before resetting ProjectServer state.
5. Kill the process listening on TCP port `24225`.
6. Restore `--context vscode` in the MCP command and restart the MCP server.
7. Verify the projects with `list_queryable_projects`, then query them from
	`fiji-llm` with `query_project`.

The installed Serena launcher starts ProjectServer automatically when port
`24225` is not already listening. ProjectServer starts the required
language servers for projects queried through `query_project`; a separate
language-server restart is not part of the normal setup procedure.

The PowerShell reset command is:

```powershell
$projectServerPids = @(Get-NetTCPConnection -LocalPort 24225 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique)
$projectServerPids | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
```

## Repository-Owned Fiji Customizations

Any Fiji-specific agent and skill are maintained by the `fiji-llm` repository and
are intentionally not duplicated here:

- `fiji-llm/doc/agents/vscode/fiji-mcp.agent.md`
- `fiji-llm/doc/agents/vscode/fiji-script-debugging/SKILL.md`

## Link Validation

Prefer links when the checkout is actively being developed so changes are picked
up immediately. Native symbolic links require Windows Developer Mode or
administrator privileges; copying is the portable fallback.

The managed discovery paths on Windows are:

- `%USERPROFILE%\\.copilot\\agents`
- `%USERPROFILE%\\.copilot\\instructions`
- `%APPDATA%\\Code\\User\\mcp.json`

Use `Get-Item` to confirm that the `agents` and `instructions` paths are
junctions or symbolic links, and verify that the expected files resolve through
them. Directory junctions are the supported no-admin fallback used by this
installation. Install the Serena launcher with `uv tool install --editable`
from `vscode/user/mcp/serena-launcher`, then copy `vscode/user/mcp/mcp.json`
into the file opened by `MCP: Open User Configuration`. Do not link Serena
configuration into `.copilot`.
