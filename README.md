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
| `JOC` | Broad communication flagship |
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
polcomm-review JOC quant article manuscript.tex
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

## Limitations

This is structured AI review, not editorial authority. It can miss problems, overstate weak ones, lag policy changes, and hallucinate issues. Always verify citations, measurements, claims, and current journal rules before acting on the output.
