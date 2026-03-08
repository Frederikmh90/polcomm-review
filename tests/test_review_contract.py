import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.review_contract import detect_stage, load_issue_schema, load_journal_manifest, parse_invocation, validate_issue


class ReviewContractTests(unittest.TestCase):
    def test_parse_full_invocation(self) -> None:
        target = parse_invocation('JournalOfCommunication quant article "papers/my paper.tex"')
        self.assertEqual(target.journal, "JournalOfCommunication")
        self.assertEqual(target.track, "quant")
        self.assertEqual(target.stage, "article")
        self.assertEqual(target.path, "papers/my paper.tex")

    def test_parse_supported_journals(self) -> None:
        for journal in (
            "PoliticalCommunication",
            "JournalOfCommunication",
            "InformationCommunicationSociety",
            "CommunicationResearch",
            "JCMC",
            "IJPP",
            "DigitalJournalism",
            "JournalismStudies",
            "NewMediaSociety",
        ):
            target = parse_invocation(f"{journal} quant article draft.tex")
            self.assertEqual(target.journal, journal)

    def test_parse_path_only(self) -> None:
        target = parse_invocation('"drafts/article.tex"')
        self.assertEqual(target.journal, "top-field")
        self.assertEqual(target.track, "auto")
        self.assertEqual(target.stage, "auto")
        self.assertEqual(target.path, "drafts/article.tex")

    def test_stage_detection(self) -> None:
        proposal = (ROOT / "tests" / "fixtures" / "proposal" / "proposal.tex").read_text(encoding="utf-8")
        dissertation = (ROOT / "tests" / "fixtures" / "dissertation" / "dissertation.tex").read_text(encoding="utf-8")
        self.assertEqual(detect_stage(proposal), "proposal")
        self.assertEqual(detect_stage(dissertation), "dissertation")

    def test_issue_schema_and_manifest(self) -> None:
        schema = load_issue_schema(ROOT / "core")
        manifest = load_journal_manifest(ROOT / "core")
        self.assertEqual(schema["title"], "Political Communication Review Issue")
        self.assertIn("NewMediaSociety", manifest["supported_journals"])
        for journal in manifest["supported_journals"]:
            self.assertEqual(manifest["journals"][journal]["verified_on"], "2026-03-08")
            self.assertGreater(len(manifest["journals"][journal]["source_urls"]), 0)

    def test_sample_outputs_validate(self) -> None:
        sample_dir = ROOT / "examples" / "sample-outputs"
        stages = set()
        tracks = set()
        for json_path in sorted(sample_dir.glob("*.json")):
            sample = json.loads(json_path.read_text(encoding="utf-8"))
            stages.add(sample["stage"])
            tracks.add(sample["track"])
            for issue in sample["issues"]:
                self.assertEqual(validate_issue(issue), [], msg=json_path.name)
        self.assertTrue({"article", "proposal", "dissertation"}.issubset(stages))
        self.assertTrue({"quant", "methods", "qual"}.issubset(tracks))

    def test_docs_include_output_contract(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        install_doc = (ROOT / "examples" / "installation.md").read_text(encoding="utf-8")
        skill = (ROOT / "templates" / "codex-skill" / "SKILL.md").read_text(encoding="utf-8")
        for doc in (readme, install_doc, skill):
            self.assertIn("review-report.md", doc)
            self.assertIn("review-report.json", doc)


if __name__ == "__main__":
    unittest.main()
