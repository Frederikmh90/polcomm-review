import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SKILL_NAME = "polcomm-review";

function packagePath(...segments) {
  return path.join(PACKAGE_ROOT, ...segments);
}

function ensureParent(filePath) {
  mkdirSync(path.dirname(filePath), { recursive: true });
}

function copyDirectory(source, destination) {
  mkdirSync(path.dirname(destination), { recursive: true });
  cpSync(source, destination, { recursive: true });
}

function replaceTarget(targetPath, force) {
  if (!existsSync(targetPath)) {
    return;
  }
  if (!force) {
    throw new Error(`Target already exists: ${targetPath}. Re-run with --force to replace it.`);
  }
  rmSync(targetPath, { recursive: true, force: true });
}

function writeTemplate(templateRelativePath, destination, replacements, force) {
  if (existsSync(destination) && !force) {
    throw new Error(`Target already exists: ${destination}. Re-run with --force to replace it.`);
  }
  ensureParent(destination);
  const template = readFileSync(packagePath("templates", templateRelativePath), "utf8");
  let output = template;
  for (const [key, value] of Object.entries(replacements)) {
    output = output.replaceAll(key, value);
  }
  writeFileSync(destination, output, "utf8");
}

export function resolveHomes(options = {}) {
  return {
    claudeHome: options.claudeHome || path.join(os.homedir(), ".claude"),
    codexHome:
      options.codexHome || process.env.CODEX_HOME || path.join(os.homedir(), ".codex"),
  };
}

function installCore(destinationSkillRoot) {
  const coreDestination = path.join(destinationSkillRoot, "core");
  replaceTarget(coreDestination, true);
  copyDirectory(packagePath("core"), coreDestination);
}

export function installClaude({ claudeHome, force = false }) {
  const skillRoot = path.join(claudeHome, "skills", SKILL_NAME);
  const commandPath = path.join(claudeHome, "commands", `${SKILL_NAME}.md`);

  replaceTarget(skillRoot, force);
  mkdirSync(skillRoot, { recursive: true });
  installCore(skillRoot);
  writeTemplate("claude-skill/SKILL.md", path.join(skillRoot, "SKILL.md"), {}, force);
  writeTemplate("claude-command/polcomm-review.md", commandPath, {}, force);

  return {
    runtime: "claude",
    destination: skillRoot,
    extraPath: commandPath,
  };
}

export function installCodex({ codexHome, force = false }) {
  const skillRoot = path.join(codexHome, "skills", SKILL_NAME);
  const agentsDir = path.join(skillRoot, "agents");

  replaceTarget(skillRoot, force);
  mkdirSync(agentsDir, { recursive: true });
  installCore(skillRoot);
  writeTemplate("codex-skill/SKILL.md", path.join(skillRoot, "SKILL.md"), {}, force);
  writeTemplate(
    "codex-skill/agents/openai.yaml",
    path.join(agentsDir, "openai.yaml"),
    {},
    force
  );

  return {
    runtime: "codex",
    destination: skillRoot,
  };
}

export function installAll({ claudeHome, codexHome, force = false }) {
  return [
    installClaude({ claudeHome, force }),
    installCodex({ codexHome, force }),
  ];
}

export function doctorSummary({ claudeHome, codexHome }) {
  const claudeSkill = path.join(claudeHome, "skills", SKILL_NAME, "SKILL.md");
  const claudeCommand = path.join(claudeHome, "commands", `${SKILL_NAME}.md`);
  const codexSkill = path.join(codexHome, "skills", SKILL_NAME, "SKILL.md");

  return {
    packageRoot: PACKAGE_ROOT,
    paths: {
      claudeHome,
      codexHome,
    },
    claude: {
      skillInstalled: existsSync(claudeSkill),
      commandInstalled: existsSync(claudeCommand),
    },
    codex: {
      skillInstalled: existsSync(codexSkill),
    },
  };
}
