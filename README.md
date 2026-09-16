# Hinerm Agent Dotfiles

Personal agent customizations used by VS Code installations.

## Layout

- `vscode/user/prompts/` contains VS Code user-level instructions and custom agents.
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
