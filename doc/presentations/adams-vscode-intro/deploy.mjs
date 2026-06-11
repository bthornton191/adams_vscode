/**
 * Deploy dist/ to the gh-pages branch of the repo.
 * Uses a temp directory with an orphan branch to avoid cloning the full repo
 * (which fails on Windows due to long filenames in the main branch).
 */
import { execSync } from "child_process";
import { mkdtempSync, cpSync, rmSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";

const distDir = join(import.meta.dirname, "dist");
const tmp = mkdtempSync(join(tmpdir(), "gh-pages-"));

try {
  const run = (cmd) => execSync(cmd, { cwd: tmp, stdio: "inherit" });

  run("git init");
  run("git checkout --orphan gh-pages");
  cpSync(distDir, tmp, { recursive: true });
  run("git add -A");
  run('git commit -m "Deploy slides"');
  run("git remote add origin https://github.com/bthornton191/adams_vscode.git");
  run("git push origin gh-pages --force");

  console.log("\nDeployed to https://bthornton191.github.io/adams_vscode/");
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
