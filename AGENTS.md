# AGENTS.md

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang, a language whose keywords, quotes, comments, and statement terminator are Unicode. Programs use `.slop` files. Run tools with `uv` from the repo root; there are no runtime dependencies.

## Project layout

- `sloperator.py` — CLI entry point; `--check` parses without executing.
- `sloperator/lexer/` — tokenization (`scanner.py:tokenize`, token types in `tokens.py`).
- `sloperator/parser/` — recursive-descent parser (`parser.py:parse`) and AST (`ast.py`); see `sloperator/parser/AGENTS.md` for parser-specific conventions.
- `sloperator/evaluator/` — tree-walking interpreter (`interpreter.py`), `Value` types, and environments.
- `sloperator/runner.py` — programmatic entry point; tests mostly call `run_source`. `sloperator/errors.py` holds the `SlopError` types.
- `tests/` — pytest suite; `examples/` — runnable `.slop` programs; `docs/spec.md` — language reference.

Pipeline: `tokenize` -> `parse` -> `Interpreter`.

## Validation

Run all four from the repo root, in this order:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

Known baseline: `ruff format --check` reports `tests/test_lexer_regression.py` as unformatted. Do not reformat unrelated files just to make the check pass.

Comparison precedence regression test: `uv run pytest tests/test_comparisons.py`.

## When to add regression tests

- Every bug fix gets a test that fails before the fix and passes after, placed in the closest `tests/test_*.py`.
- Any behavior or diagnostic change in the lexer, parser, or evaluator needs a test asserting the observable result. Diagnostics are asserted by exact message and line number, so update existing expectations in the same change.
- A new token, grammar rule, AST node, or value type needs coverage at each affected stage.
- New `examples/*.slop` programs are exercised by `tests/test_examples.py`; they must exit 0 and print something.
- Prefer extending an existing focused test file over adding a new one, and run the full suite before submitting.

## Language behavior

SlopLang's language behavior — grammar, types, scoping, errors, and semantics — is defined in [`docs/spec.md`](docs/spec.md). Read the relevant section before changing the lexer, parser, or evaluator, and update the spec in the same change when behavior changes.
