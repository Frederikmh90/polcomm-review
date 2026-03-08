# Installation Notes

Install Claude assets:

```bash
npx polcomm-review install claude
```

Install Codex assets:

```bash
npx polcomm-review install codex
```

Install both:

```bash
npx polcomm-review install all
```

Overwrite existing installed assets with `--force`.

The installed prompts should write:

- `review-report.md`
- `review-report.json`

Do not merely describe the outputs. If the environment cannot write files, the runtime should return both artifacts in chat.
