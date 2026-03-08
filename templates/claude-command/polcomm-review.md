---
description: Run a stage-aware political communication pre-submission audit with journal personas and evidence-grounded issue reporting
argument-hint: [journal] [track] [stage] [path]
---

Use the installed `polcomm-review` skill to review a political communication manuscript.

Read these files from the installed skill directory:

1. `../skills/polcomm-review/core/invocation-spec.md`
2. `../skills/polcomm-review/core/journal-manifest.json`
3. `../skills/polcomm-review/core/paper-discovery.md`
4. `../skills/polcomm-review/core/track-stage-rules.md`
5. `../skills/polcomm-review/core/issue-taxonomy.md`
6. `../skills/polcomm-review/core/references/guardrails.md`
7. `../skills/polcomm-review/core/references/journal-signals.md`
8. `../skills/polcomm-review/core/references/journal-personas.md`
9. all files in `../skills/polcomm-review/core/modules/`
10. `../skills/polcomm-review/core/report-template.md`

Write `review-report.md` and `review-report.json`. Do not merely describe the outputs. If the environment cannot write files, say so explicitly and return both artifacts in-chat.
