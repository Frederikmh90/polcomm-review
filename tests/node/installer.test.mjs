import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";

import { doctorSummary, installAll, installClaude, installCodex } from "../../src/install.js";

function withTempDirs(run) {
  const root = mkdtempSync(path.join(os.tmpdir(), "polcomm-review-"));
  const claudeHome = path.join(root, ".claude");
  const codexHome = path.join(root, ".codex");
  try {
    run({ root, claudeHome, codexHome });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

withTempDirs(({ claudeHome, codexHome }) => {
  const claudeResult = installClaude({ claudeHome, force: true });
  const codexResult = installCodex({ codexHome, force: true });
  assert.equal(existsSync(path.join(claudeResult.destination, "SKILL.md")), true);
  assert.equal(existsSync(path.join(codexResult.destination, "agents", "openai.yaml")), true);
  assert.match(readFileSync(path.join(claudeHome, "commands", "polcomm-review.md"), "utf8"), /polcomm-review/);

  installAll({ claudeHome, codexHome, force: true });
  const summary = doctorSummary({ claudeHome, codexHome });
  assert.equal(summary.claude.skillInstalled, true);
  assert.equal(summary.claude.commandInstalled, true);
  assert.equal(summary.codex.skillInstalled, true);
});

console.log("ok - installer writes self-contained polcomm-review assets");
