# Hinerm Agent Dotfiles

Personal agent customizations used by VS Code installations.

## Layout

- `vscode/user/agents/` contains Copilot user-level custom agents.
- `vscode/user/instructions/` contains Copilot user-level instructions.
- `vscode/user/mcp/` contains the synchronized VS Code MCP configuration and
	the cross-platform Serena launcher package.
- `AGENTS.md` documents the maintenance rules for this repository.

## Managed Files

The canonical agent and instruction files are tracked here and remain
available at their normal Copilot Agent Host discovery paths. The MCP file is
copied into the VS Code user configuration:

- `vscode/user/agents/` -> `%USERPROFILE%\\.copilot\\agents\\`
- `vscode/user/instructions/` -> `%USERPROFILE%\\.copilot\\instructions\\`
- `vscode/user/mcp/mcp.json` -> the file opened by VS Code's `MCP: Open User Configuration`
- `vscode/user/mcp/serena-launcher/` -> installed with `uv tool install`

Edit the canonical files in this repository. The user-level agent and
instruction paths are directory junctions into this tree, so Copilot continues
to discover them normally.

The VS Code MCP configuration is synchronized normally. Copy it once into the
VS Code user configuration rather than linking it into the platform-specific
Copilot directory.

## Windows Link Note

This installation uses directory junctions for the managed `agents` and
`instructions` directories because native symbolic-link creation requires
Windows Developer Mode or administrator privileges. Junctions provide the same
path redirection for this local setup. After enabling Developer Mode, the
junctions can be replaced with native symbolic links if desired.

Do not store API keys, tokens, passwords, or other secrets in this repository.

The former `%APPDATA%\\Code\\User\\prompts` path was used for Local-agent
prompt files. Prompt files are deprecated for Agent Host sessions, so it is not
a managed path for these Copilot customizations.

## Serena MCP

Install the launcher from the dotfiles checkout:

```sh
cd vscode/user/mcp/serena-launcher
uv tool install --editable . --force
```

If VS Code cannot find the installed command, run `uv tool update-shell` and
restart VS Code so its process environment includes the uv tool directory.

Then copy `vscode/user/mcp/mcp.json` into the file opened by VS Code's
`MCP: Open User Configuration` command. Settings Sync can synchronize that
single configuration across platforms because the server entry uses the
platform-neutral `serena-mcp-launcher` command and `${userHome}` variable.

The launcher starts Serena's ProjectServer automatically when needed, then
launches the MCP server against the Fiji LLM project under the user's profile.

Do not add Serena to `~/.copilot/mcp-config.json`; that configuration is owned
by the Copilot CLI/Agent Host and causes Serena to appear under the Copilot
runtime. Keep the VS Code user `mcp.json` as the single source for both shared
servers.

Keep `fiji-llm` active during normal work and query local dependency checkouts
through Serena's `query_project` tool. When a checkout needs to be added to
Serena's project list, temporarily use the `agent` context, activate each
absolute checkout root and then `fiji-llm`, stop the MCP server, kill the
ProjectServer process listening on TCP port `24225`, restore the `vscode`
context, and restart the MCP server. ProjectServer starts the required
language servers for projects queried through `query_project`; no separate
language-server restart is normally needed. See `AGENTS.md` for the complete
procedure.
