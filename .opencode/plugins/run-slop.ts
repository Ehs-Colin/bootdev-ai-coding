import { spawn } from "node:child_process";
import { resolve } from "node:path";

import { Plugin } from "@opencode/plugin";

interface RunResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function run(command: string, args: string[], cwd: string): Promise<RunResult> {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(command, args, { cwd });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk: Buffer) => {
      stdout += chunk.toString();
    });

    child.stderr.on("data", (chunk: Buffer) => {
      stderr += chunk.toString();
    });

    child.on("error", reject);

    child.on("close", (code: number | null) => {
      resolvePromise({
        stdout,
        stderr,
        exitCode: code ?? 1,
      });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a Sloperator program (.slop file) with uv and return its stdout, stderr, and exit code as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file to run.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const projectRoot = ctx.location.project.directory;
          const file = resolve(projectRoot, path);

          const result = await run(
            "uv",
            ["run", "--no-active", "sloperator.py", file],
            projectRoot,
          );

          return { content: JSON.stringify(result) };
        },
      });
    });
  },
});
