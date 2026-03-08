# PolComm Review

A structured, LLM-agnostic pre-submission audit for political communication and adjacent communication manuscripts. Use it for a systematic review pass before circulation or submission.

PolComm Review adapts the package shape pioneered by [cmertdalli/polisci-review](https://github.com/cmertdalli/polisci-review) and applies it to communication journals with journal-aware personas, stage-aware standards, and evidence-grounded issue reporting.

## What It Checks

The review battery runs nine modules:

1. **Contribution and literature positioning**
2. **Writing, structure, and framing**
3. **Internal consistency and citation integrity**
4. **Theory, concepts, and scope conditions**
5. **Measurement and data construction**
6. **Design and identification**
7. **Track-specific technical audit**
8. **Transparency, reproducibility, ethics, and AI policy**
9. **Journal fit and Reviewer #2 assessment**

Every issue includes a module label, location anchor, evidence status, journal-policy reference, and a recommended fix.

## Supported Journals

| Journal | Role |
|---------|------|
| `PoliticalCommunication` | Political communication flagship |
| `JournalOfCommunication` | Broad communication flagship |
| `InformationCommunicationSociety` | Digital society and communication generalist |
| `CommunicationResearch` | Empirical communication research flagship |
| `JCMC` | Digital communication flagship |
| `IJPP` | Press and politics flagship |
| `DigitalJournalism` | Digital journalism flagship |
| `JournalismStudies` | Journalism studies generalist |
| `NewMediaSociety` | New media and society flagship |

Source URLs and verification dates live in [`core/journal-manifest.json`](./core/journal-manifest.json).

### Journal-Agnostic Mode

Running without a journal argument applies a `top-field` communication standard: strong contribution, honest evidence, legible methods, and current best practices without outlet-specific enforcement.

## Quick Start

Install the Claude adapter:

```bash
npx polcomm-review install claude
```

Install the Codex adapter:

```bash
npx polcomm-review install codex
```

Install both:

```bash
npx polcomm-review install all
```

Inspect detected install paths:

```bash
npx polcomm-review doctor
```

## How to Use

```text
polcomm-review [JOURNAL] [TRACK] [STAGE] [PATH]
```

**Tracks**: `methods`, `quant`, `formal`, `qual`, `mixed` (default: `auto`)

**Stages**: `article`, `proposal`, `dissertation` (default: `auto`)

**Defaults**: journal=`top-field`, track=`auto`, stage=`auto`

Examples:

```text
polcomm-review JournalOfCommunication quant article manuscript.tex
polcomm-review PoliticalCommunication qual dissertation.tex
polcomm-review manuscript.tex
```

## Supported Manuscript Formats

The workflow is LaTeX-first. If `.tex` source exists, that is the preferred review path. It can also review:

- `.docx`
- `.md`
- `.txt`
- `.pdf` with readable text or OCR

## Output Contract

When the runtime allows file writes, the installed skill should write two files by default:

- `review-report.md` following [`core/report-template.md`](./core/report-template.md)
- `review-report.json` following [`core/issue-schema.json`](./core/issue-schema.json)

By default these files should be written next to the main manuscript. If the environment cannot write files, the skill should return the same content in the chat and say that file output was unavailable.

Sample outputs live in [`examples/sample-outputs/`](./examples/sample-outputs/).

## Choosing a Model

The framework is model-agnostic. Claude is the default recommendation because it currently gives the strongest balance of instruction-following and long-context reading for this workflow.

That said, model performance changes fast. Before choosing a model for production use:

1. Check the [benchmark viewer](https://petergpt.github.io/bullshit-benchmark/viewer/index.v2.html) for current rankings. Models with high "Clear Pushback" rates are better at identifying real problems rather than inventing issues.
2. Prefer models with strong instruction-following and long-context capabilities. Check the benchmark link above for current leaders; specific model names go stale quickly.
3. Test with your own manuscripts. No benchmark replaces domain-specific evaluation.

Do not treat any model recommendation as permanent.

## Repository Layout

```text
core/        shared review contract, journal manifest, personas, and modules
adapters/    runtime-specific source files
examples/    installation docs, sample manuscripts, and sample outputs
templates/   packaged Claude and Codex adapter templates
tests/       contract, installer, and fixture validation
```

## Why This Exists

This project builds on two prior inspirations. First, Claes Bäckman's econ-focused [AI-research-feedback](https://github.com/claesbackman/AI-research-feedback/tree/main) introduced the idea of structured AI manuscript review with parallel review agents. Second, Cem Mert Dalli's [`polisci-review`](https://github.com/cmertdalli/polisci-review) translated that idea into a journal-aware, packaged skill structure for political science. `polcomm-review` adapts that architecture for political communication and adjacent communication journals, using a 9-module review battery, journal-specific personas, stage-aware standards, and a machine-readable issue contract. The aim is a structured review framework for communication research rather than a generic manuscript-commenting prompt.

## Limitations

This is structured AI review, not editorial guidance from any journal. It can:

- miss obvious problems or overstate weak ones
- lag behind journal policy changes
- hallucinate issues that do not exist in the manuscript
- fail to catch subtle methodological flaws that a human reviewer would spot

Always verify citations, formulas, design claims, and current journal rules before acting on the output. Each report includes a limitations note for that reason.

## Installation Details

See [`examples/installation.md`](./examples/installation.md) for adapter-specific install behavior and overwrite behavior.

## Contact

Suggestions, bug reports, and journal-profile contributions are welcome. Reach Frederik Henriksen at `frmohe@ruc.dk`.
