import {
  doctorSummary,
  installAll,
  installClaude,
  installCodex,
  resolveHomes,
} from "./install.js";

function printHelp() {
  console.log(`polcomm-review

Usage:
  polcomm-review install <claude|codex|all> [--claude-home PATH] [--codex-home PATH] [--force]
  polcomm-review doctor [--claude-home PATH] [--codex-home PATH]
  polcomm-review help

Examples:
  npx polcomm-review install claude
  npx polcomm-review install codex
  npx polcomm-review install all --force
  npx polcomm-review doctor
`);
}

function parseOptions(tokens) {
  const options = {
    force: false,
    claudeHome: undefined,
    codexHome: undefined,
  };
  const positionals = [];
  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    if (token === "--force") {
      options.force = true;
      continue;
    }
    if (token === "--claude-home") {
      options.claudeHome = tokens[index + 1];
      index += 1;
      continue;
    }
    if (token === "--codex-home") {
      options.codexHome = tokens[index + 1];
      index += 1;
      continue;
    }
    positionals.push(token);
  }
  return { options, positionals };
}

function printDoctor(summary) {
  console.log("polcomm-review doctor");
  console.log(`Package root: ${summary.packageRoot}`);
  console.log(`Claude home: ${summary.paths.claudeHome}`);
  console.log(`Codex home: ${summary.paths.codexHome}`);
  console.log(
    `Claude skill: ${summary.claude.skillInstalled ? "installed" : "missing"}`
  );
  console.log(
    `Claude command: ${summary.claude.commandInstalled ? "installed" : "missing"}`
  );
  console.log(
    `Codex skill: ${summary.codex.skillInstalled ? "installed" : "missing"}`
  );
}

function printInstallResult(result) {
  console.log(`Installed ${result.runtime} assets.`);
  console.log(`Destination: ${result.destination}`);
  if (result.extraPath) {
    console.log(`Extra path: ${result.extraPath}`);
  }
}

export async function main(argv) {
  const { options, positionals } = parseOptions(argv);
  const command = positionals[0] || "help";

  if (command === "help" || command === "--help" || command === "-h") {
    printHelp();
    return;
  }

  if (command === "doctor") {
    const paths = resolveHomes(options);
    printDoctor(doctorSummary(paths));
    return;
  }

  if (command !== "install") {
    printHelp();
    throw new Error(`Unknown command: ${command}`);
  }

  const runtime = positionals[1];
  if (!runtime || !["claude", "codex", "all"].includes(runtime)) {
    printHelp();
    throw new Error("Install target must be one of: claude, codex, all");
  }

  const paths = resolveHomes(options);
  if (runtime === "claude") {
    printInstallResult(installClaude({ ...paths, force: options.force }));
    return;
  }
  if (runtime === "codex") {
    printInstallResult(installCodex({ ...paths, force: options.force }));
    return;
  }

  for (const result of installAll({ ...paths, force: options.force })) {
    printInstallResult(result);
  }
}
