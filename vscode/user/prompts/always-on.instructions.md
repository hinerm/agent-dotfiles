---
name: "Always-On User Rules"
description: "Personal rules for all coding-agent tasks."
applyTo: "**"
---

- Never search or read `~/.m2` or dependency caches.
- After creating new files, run `mvn license:update-file-header` to apply the license header instead of generating it manually.
- If the user names a local path, inspect that path directly before doing a broader search.
- When you are the primary coding agent and an external Java API or resource lookup is needed, invoke the `dependency-source-research` agent first when it is available. Provide the workspace path and the dependency, symbol, or resource to investigate, then use its report as evidence before exploring broadly yourself. This delegation rule does not apply inside that research agent.
- When an external dependency's behavior or API matters, first use relevant source attachments or excerpts provided by the user. If they are insufficient, derive the dependency's group, artifact, and module from the build descriptor and inspect local source under `~/code` before using any other source. Search organization roots and nested module descriptors, not only repository names that exactly match Maven artifacts. Account for layouts such as `~/code/scijava/*`, `~/code/imagej/*`, and multi-module repositories such as `~/code/langchain4j/langchain4j/*`; on Windows, `~/code` may be `C:\Users\<user>\code`.
- When a candidate checkout is found, inspect its root or module `pom.xml` and only the relevant source, tests, or history. Do not add sibling repositories as workspace folders or build them just to inspect an API. A version mismatch is not evidence that the checkout is absent; report the actual local version separately.
- If no plausible local checkout is found, state which organization roots and nested module descriptors were checked, then stop dependency-source lookup. Do not substitute dependency caches or remote source; user-provided source attachments remain valid evidence.
- For compile or type errors in edited files, check VS Code editor diagnostics first. Run workspace-wide `get_errors` by omitting `filePaths` entirely, exactly as `{}`, then filter the returned diagnostics to the edited file. Do not pass a file or folder through `filePaths` for this workflow; use `filePaths` only when the user explicitly requests a scoped diagnostics check, because file-scoped diagnostics can return false negatives. Prefer this validation over running `mvn compile` or `mvn test-compile` redundantly.
- Use Maven when project-level behavior needs validation, such as tests, annotation processing, generated sources, dependency wiring, packaging, or when editor diagnostics are unavailable or incomplete.
