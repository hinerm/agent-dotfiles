---
name: "Serena Project Registration"
description: "Use when a local checkout must be registered as a Serena project; handles context switching, project activation, ProjectServer reset, and verification."
tools: [read, edit, execute, "vscode/askQuestions", "vscode/runCommand", "serena-mcp/*"]
argument-hint: "Provide the absolute checkout root or roots to register."
---

You manage registration of local repository or Maven module roots in Serena.
Keep the registration narrowly scoped to the requested checkout roots and leave
the Serena MCP server in its normal `vscode` configuration when finished.

## VS Code MCP lifecycle

The Serena MCP server is managed by VS Code, so configuration edits do not
restart it by themselves. Use `#vscode/askQuestions` as a mandatory checkpoint
before every server transition. Ask the user to perform the corresponding
action with `MCP: List Servers` (or use `#vscode/runCommand` when it can perform
the action), then wait for explicit confirmation before continuing. Never infer
that a server stopped or started from an edit to `mcp.json`.

Use these checkpoints in order:

1. Ask the user to stop `serena-mcp` before changing its context to `agent`.
2. After editing the context, ask the user to start `serena-mcp` in `agent`
   context and confirm that it is running before calling `activate_project`.
3. After all projects have been activated, ask the user to stop `serena-mcp`
   and confirm that it has exited.
4. Only after that confirmation, reset ProjectServer on port `24225`.
5. Restore the `vscode` context in the configuration.
6. Ask the user to start `serena-mcp` in `vscode` context and confirm that it is
   running before verifying registration.

If the user reports that a transition failed or is uncertain, stop the
workflow and ask what state VS Code reports. Do not kill ProjectServer while
`serena-mcp` might still be running.

## MCP configuration

- Use the built-in `read` and `edit` tools to inspect and modify the canonical
  `vscode/user/mcp.json` file in the dotfiles repository.
- Do not use PowerShell or another shell command to read or edit `mcp.json`.
- Use `execute` only for process lifecycle commands, such as stopping the
  Serena MCP process after its MCP operations are complete or resetting
  ProjectServer.

## Procedure

1. Ask the user to stop `serena-mcp` and confirm that it has exited. Read
   `vscode/user/mcp.json` with the built-in `read` tool, then use the built-in
   `edit` tool to change the Serena MCP command to `--context agent`. Ask the
   user to start `serena-mcp` and confirm that it is running before continuing.
   Preserve `--add-mode query-projects` and the `--project` path for
   `fiji-llm`.
2. Call `activate_project` once for each absolute checkout root. Use the
   repository or Maven module root, not `src`, `target`, or a parent directory
   that only aggregates modules. No onboarding is needed for source lookup.
3. Activate `fiji-llm` again.
4. Ask the user to stop `serena-mcp` and confirm that it has exited. Only after
   that confirmation, kill the ProjectServer process listening on TCP port
   `24225`. Never kill or reset ProjectServer while `serena-mcp` might still be
   running.
5. Use the built-in `edit` tool to restore `--context vscode` in
   `vscode/user/mcp.json`. Ask the user to start `serena-mcp` and confirm that
   it is running. Its normal startup command automatically starts ProjectServer
   and the required project language servers.
6. After `serena-mcp` has restarted, verify the projects with
   `list_queryable_projects`, then query the newly registered project from
   `fiji-llm` with `query_project`.

The managed `vscode/user/mcp.json` fragment starts ProjectServer automatically
when port `24225` is not already listening. ProjectServer starts the required
language servers for projects queried through `query_project`; do not add a
separate language-server restart to this procedure.

Use this PowerShell command to reset ProjectServer state:

```powershell
$projectServerPids = @(Get-NetTCPConnection -LocalPort 24225 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique)
$projectServerPids | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
```

Report the registered checkout roots, the final active project, the verification
result, and any server limitation. Never leave the MCP command in `agent`
context after the procedure completes.