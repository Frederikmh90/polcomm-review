"""Canonical data contracts and parsing logic for PolComm Review."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import json
from pathlib import Path
import shlex
from typing import Any

TRACK_VALUES = {"auto", "methods", "quant", "formal", "qual", "mixed"}
STAGE_VALUES = {"auto", "article", "proposal", "dissertation"}
SEVERITY_VALUES = {"critical", "major", "minor"}
CATEGORY_VALUES = {
    "fit",
    "contribution",
    "literature",
    "theory",
    "concept",
    "measurement",
    "data",
    "design",
    "identification",
    "evidence",
    "transparency",
    "ethics",
    "policy",
    "consistency",
    "style",
}
MODULE_VALUES = {
    "contribution-literature",
    "writing-framing",
    "consistency-citations",
    "theory-concepts-scope",
    "measurement-data",
    "design-identification",
    "technical-audit",
    "transparency-ethics-policy",
    "journal-fit-reviewer-2",
}
EVIDENCE_STATUS_VALUES = {
    "verified inconsistency",
    "inferred absence",
    "needs human check",
}
CONFIDENCE_VALUES = {"high", "medium", "low"}

_TRACK_LOOKUP = {value: value for value in TRACK_VALUES}
_STAGE_LOOKUP = {value: value for value in STAGE_VALUES}

_PROPOSAL_MARKERS = (
    "proposal",
    "prospectus",
    "planned study",
    "will estimate",
    "we propose",
    "expected contribution",
    "anticipated contribution",
)
_DISSERTATION_MARKERS = (
    "dissertation",
    "thesis",
    "committee",
    "chapter 1",
    "chapter 2",
    "paper 1",
    "paper 2",
    "paper 3",
)


def _core_path(root: Path | None = None) -> Path:
    return root or Path(__file__).resolve().parent


def _normalize_journal_token(token: str) -> str:
    return "".join(character for character in token.lower() if character.isalnum())


@lru_cache(maxsize=1)
def load_journal_manifest(root: Path | None = None) -> dict[str, Any]:
    manifest_path = _core_path(root) / "journal-manifest.json"
    with manifest_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _journal_lookup(root: Path | None = None) -> dict[str, str]:
    manifest = load_journal_manifest(root)
    lookup: dict[str, str] = {"topfield": "top-field"}
    for journal in manifest["supported_journals"]:
        lookup[_normalize_journal_token(journal)] = journal
    for alias, journal in manifest["aliases"].items():
        lookup[_normalize_journal_token(alias)] = journal
    return lookup


JOURNAL_VALUES = set(load_journal_manifest()["supported_journals"]) | {"top-field"}


@dataclass
class InvocationTarget:
    journal: str = "top-field"
    track: str = "auto"
    stage: str = "auto"
    path: str | None = None
    warnings: list[str] = field(default_factory=list)


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_invocation(arguments: str) -> InvocationTarget:
    target = InvocationTarget()
    raw = arguments.strip()
    if not raw:
        return target

    journal_lookup = _journal_lookup()
    tokens = [_strip_quotes(token) for token in shlex.split(raw, posix=False)]
    path_start = len(tokens)

    for index, token in enumerate(tokens):
        normalized = _normalize_journal_token(token.strip())
        if normalized in journal_lookup and target.journal == "top-field":
            target.journal = journal_lookup[normalized]
            continue

        lowered = token.strip().lower()
        if lowered in _TRACK_LOOKUP and target.track == "auto":
            target.track = _TRACK_LOOKUP[lowered]
            continue
        if lowered in _STAGE_LOOKUP and target.stage == "auto":
            target.stage = _STAGE_LOOKUP[lowered]
            continue

        path_start = index
        break

    if path_start < len(tokens):
        target.path = " ".join(tokens[path_start:])

    return target


def detect_stage(text: str) -> str:
    lowered = text.lower()
    proposal_hits = sum(1 for marker in _PROPOSAL_MARKERS if marker in lowered)
    dissertation_hits = sum(1 for marker in _DISSERTATION_MARKERS if marker in lowered)
    if proposal_hits >= dissertation_hits and proposal_hits > 0:
        return "proposal"
    if dissertation_hits > 0:
        return "dissertation"
    return "article"


def load_issue_schema(root: Path | None = None) -> dict[str, Any]:
    schema_path = _core_path(root) / "issue-schema.json"
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_issue(issue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "module",
        "journal_policy_ref",
        "location",
        "evidence",
        "severity",
        "category",
        "why_it_matters",
        "recommended_fix",
        "confidence",
    ]
    for key in required:
        if key not in issue:
            errors.append(f"Missing required field: {key}")

    if issue.get("module") not in MODULE_VALUES:
        errors.append("module must be a supported review module")
    policy_ref = issue.get("journal_policy_ref")
    if not isinstance(policy_ref, str) or not policy_ref.strip():
        errors.append("journal_policy_ref must be a non-empty string")

    location = issue.get("location", {})
    if not isinstance(location, dict):
        errors.append("location must be an object")
    else:
        for key in ("file", "anchor"):
            if not location.get(key):
                errors.append(f"location.{key} is required")

    evidence = issue.get("evidence", {})
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
    else:
        if evidence.get("status") not in EVIDENCE_STATUS_VALUES:
            errors.append("evidence.status must be a supported evidence status")
        if not evidence.get("basis"):
            errors.append("evidence.basis is required")

    if issue.get("severity") not in SEVERITY_VALUES:
        errors.append("severity must be critical, major, or minor")
    if issue.get("category") not in CATEGORY_VALUES:
        errors.append("category must be a supported taxonomy value")
    if issue.get("confidence") not in CONFIDENCE_VALUES:
        errors.append("confidence must be high, medium, or low")
    for key in ("why_it_matters", "recommended_fix"):
        value = issue.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a non-empty string")

    return errors
