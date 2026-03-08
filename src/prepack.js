import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const source = path.join(PACKAGE_ROOT, "templates");
const target = path.join(PACKAGE_ROOT, "adapters");

if (existsSync(target)) {
  rmSync(target, { recursive: true, force: true });
}
mkdirSync(target, { recursive: true });
cpSync(source, target, { recursive: true });
