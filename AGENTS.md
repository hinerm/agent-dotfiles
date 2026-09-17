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

## Serena Project Registration

Serena uses one active project for the repository being edited and can query
additional registered projects as external source checkouts. Keep `fiji-llm`
active in normal work; register dependency modules separately and query them
with `query_project` rather than switching the active project.

Register the checkout root or Maven module root, not `src`, `target`, or a
parent directory that only aggregates modules.

When the Serena `activate_project` tool is available, prefer it for
registration. Call it once per absolute checkout path, for example:

```json
{"project":"C:\\Users\\<user>\\code\\scijava\\script-editor"}
```

This creates the Serena project when needed and activates it, without the
interactive language-selection prompts. Repeat for each dependency, then
activate `fiji-llm` again. Dependency projects do not need onboarding just to
support source lookup.

Use one unique project name per checkout. Existing registrations do not need
to be recreated.

`activate_project` does not take a language argument. To force a checkout to
use Java, set `language_servers` to `- java` in that project's
`.serena/project.yml`, then restart the relevant Serena language server.
When resetting Serena, do not restart or kill only its ProjectServer; stop the
MCP server first, then restart ProjectServer and the MCP server in that order.

The Serena MCP server should start with `--add-mode query-projects` and
`--project <fiji-llm-path>`. Cross-project symbol queries also require the
Serena ProjectServer, started separately with:

```powershell
uv run --with serena-agent serena start-project-server
```

The managed `vscode/user/mcp.json` fragment starts ProjectServer automatically
when port `24225` is not already listening. After adding registrations,
restart the MCP server and verify them with `list_queryable_projects` before
using `query_project`.

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
