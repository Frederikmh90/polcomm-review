# Invocation Spec

Canonical contract:

```text
polcomm-review [JOURNAL] [TRACK] [STAGE] [PATH]
```

## Parsing Rules

- Parse tokens from left to right until the first unrecognized token. Treat the remaining text as `PATH`.
- Journals are case-insensitive.
- If no journal is supplied, use `top-field`.
- If no track is supplied, use `auto`.
- If no stage is supplied, use `auto`.
- Use [`journal-manifest.json`](./journal-manifest.json) as the allowlist for supported public journals and aliases.

## Supported Journals

- `PoliticalCommunication`
- `JournalOfCommunication`
- `InformationCommunicationSociety`
- `CommunicationResearch`
- `JCMC`
- `IJPP`
- `DigitalJournalism`
- `JournalismStudies`
- `NewMediaSociety`

## Supported Tracks

- `methods`
- `quant`
- `formal`
- `qual`
- `mixed`

`auto` should prefer explicit manuscript cues first and fall back to `methods` only when the evidence is ambiguous.

## Supported Stages

- `article`
- `proposal`
- `dissertation`

`auto` should infer stage from manuscript cues before defaulting to `article`.

## Output Requirements

Every run should emit:

- one Markdown report using [`report-template.md`](./report-template.md)
- one machine-readable issue artifact whose issues conform to [`issue-schema.json`](./issue-schema.json)
