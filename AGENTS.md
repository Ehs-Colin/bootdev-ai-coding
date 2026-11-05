# AGENTS.md

Sloperator is a Python tree-walking interpreter for SlopLang, a deliberately odd language whose keywords, quotes, comments, and statement terminator are Unicode. Source files use `.slop`.

## Setup and commands

- Python 3.13 is pinned in `.python-version`; always invoke tools through `uv` from the repo root (there are no runtime dependencies).
- Run a program: `uv run sloperator.py path/to/program.slop`
- Parse-only check (does not execute): `uv run sloperator.py --check path/to/program.slop`
- Full suite: `uv run pytest`
- One test: `uv run pytest tests/test_cli.py::test_division_by_zero_reports_a_runtime_error`
- Validation order: `uv run pytest`, `uv run ruff format --check`, `uv run ruff check`, `uv run ty check`.
- The bundled `validate` skill (`.agents/skills/validate/SKILL.md`) omits `ty check`; run it too.
- Known baseline: `ruff format --check` currently reports `tests/test_lexer_regression.py` as unformatted. Do not reformat unrelated files just to make validation green.

## Architecture

- `sloperator.py` is only the CLI: `--check` may appear anywhere, exactly one file is accepted, exit codes are 0 success, 1 language error, 2 usage/I/O error.
- `sloperator/runner.py` is the programmatic entrypoint. `run_program`/`check_program` return a `SlopError | None`; `run_source` returns `RunResult(stdout, stderr, exit_code)`. Tests mostly use `run_source`.
- Pipeline: `lexer/scanner.py:tokenize` -> `parser/parser.py:parse` -> `evaluator/interpreter.py:Interpreter`. AST nodes are in `parser/ast.py`, the `Value` union in `evaluator/values.py`, and line-only `SlopError` subtypes in `errors.py`.
- `docs/spec.md` is the language reference. Read the relevant section before changing lexer/parser/evaluator behavior and keep it in sync.

## SlopLang editing gotchas

- Syntax is strict Unicode: `—` starts a comment, `“ ”` delimit strings (straight quotes are errors), `✨` terminates statements, `✅`/`❌` are booleans. Emoji may be followed by U+FE0F. Identifiers are ASCII; numbers are arbitrary-precision ints with no floats.
- Statements end in `✨` except block-closing `}`. `ship` is only valid inside `clanker`; `clanker` declarations are only valid at top level.
- No implicit conversions: conditions and `&&`/`||` require booleans, `+` requires two numbers or two strings, and division truncates toward zero.
- The lexer intentionally emits hints for common mistakes (`"`, `;`, `//`, en dash). Tests assert exact error messages and line numbers, so update tests with any diagnostic change.
- Call depth is capped at 500 and Python `RecursionError` is converted to a runtime error; the CLI must never expose a traceback.
- A new token requires coordinated changes in `lexer/tokens.py`, `lexer/scanner.py`, the parser, and the evaluator, plus tests for each stage.
- `tests/test_examples.py` runs every `examples/*.slop` file and requires exit 0 and non-empty stdout. New examples must print something.

## Current implementation/spec divergences

- `ralph` executes its body once before checking the condition (`Interpreter.execute`), while `docs/spec.md` says the condition is checked first. Verify before relying on loop semantics; no test covers an initially-false condition.
- A bare `{ ... }` block is parented to the global environment, not the enclosing function/block scope. This is untested; the spec says every brace block is a lexical scope.

## Tooling

- OpenCode exposes `run_slop` from `.opencode/plugins/run-slop.ts`, which runs a `.slop` path from the project root via `uv run --no-active`. Prefer it for quick behavior checks.
- Playground: `uv run playground/server.py [port]` (default 8080). It serves `playground/index.html` and POST `/run`, shelling out to the CLI with a 5-second timeout and appending results to `logs/runs.log` (gitignored).
