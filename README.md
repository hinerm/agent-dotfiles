# Hinerm Agent Dotfiles

Personal agent customizations used by VS Code installations.

## Layout

- `vscode/user/prompts/` contains VS Code user-level instructions and custom agents.
- `vscode/user/mcp.json` is a minimal merge fragment for the Serena MCP server.
- `AGENTS.md` documents the maintenance rules for this repository.

## Managed Files

The canonical files are tracked here and remain available at their normal discovery paths:

- `vscode/user/prompts/` -> `%APPDATA%\\Code\\User\\prompts\\`

Edit the canonical files in this repository. The original paths are links into this tree, so VS Code and Copilot continue to discover them normally.

## Windows Link Note

This installation uses a directory junction for the managed prompts directory
because native symbolic-link creation requires Windows Developer Mode or
administrator privileges. Junctions provide the same path redirection for this
local directory. After enabling Developer Mode, the junction can be replaced
with a native symbolic link if desired.

Do not store API keys, tokens, passwords, or other secrets in this repository.

## Serena MCP

The Serena configuration in `vscode/user/mcp.json` starts the MCP server in
the `vscode` context with `query-projects` enabled. It starts the Serena
ProjectServer automatically when needed, then launches the MCP server against
the Fiji LLM project under the user's profile.

Keep `fiji-llm` active during normal work and query local dependency checkouts
through Serena's `query_project` tool. When a checkout needs to be added to
Serena's project list, temporarily use the `agent` context, activate each
absolute checkout root and then `fiji-llm`, stop the MCP server, kill the
ProjectServer process listening on TCP port `24225`, restore the `vscode`
context, and restart the MCP server. ProjectServer starts the required
language servers for projects queried through `query_project`; no separate
language-server restart is normally needed. See `AGENTS.md` for the complete
procedure.
