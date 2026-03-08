# Paper Discovery

Preferred input order:

1. Main `.tex` manuscript when available
2. Linked section files included with `\input{}` or `\include{}`
3. `.md` or `.txt`
4. `.docx`
5. text-readable `.pdf`

Rules:

- Prefer `.tex` whenever both source and rendered files exist.
- When a main TeX file includes other files, read the linked components before reviewing.
- If a `.docx` or `.pdf` cannot be extracted reliably, state that and request exported text rather than guessing.
- Keep citations, tables, figures, and appendices in scope when they are available.
- If there are multiple candidate entrypoints, prefer the file with `\documentclass` or the clearest article-level structure.
