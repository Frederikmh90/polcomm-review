---
name: polcomm-review
description: Run a political communication pre-submission audit with journal-aware personas, stage-aware standards, and evidence-grounded issue reporting.
metadata:
  short-description: Political communication pre-submission audit
---

# PolComm Review

This installed skill is self-contained.

Read the canonical files in this order:

1. `./core/invocation-spec.md`
2. `./core/journal-manifest.json`
3. `./core/paper-discovery.md`
4. `./core/track-stage-rules.md`
5. `./core/issue-taxonomy.md`
6. `./core/references/guardrails.md`
7. `./core/references/journal-signals.md`
8. `./core/references/journal-personas.md`
9. all relevant files in `./core/modules/`
10. `./core/report-template.md`

Workflow:

1. Parse user arguments using the canonical invocation contract.
2. Discover the manuscript and linked component files.
3. Detect stage and track when omitted.
4. Apply the selected journal persona and the 9-module audit structure.
5. Write `review-report.md` and `review-report.json`.
6. Briefly confirm the output paths.
