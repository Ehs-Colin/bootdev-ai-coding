---
name: create-test-program
description: Create a SlopLang example program and an exact-output test for a language feature
---

# Create Test Program

Given a SlopLang language feature, add a runnable example and an exact-output test for it.

1. Read `docs/spec.md` for the feature's syntax, semantics, precedence, and error behavior before writing anything.
2. Write a focused example program in `examples/`, named after the feature (for example `examples/string_addition.slop`). Use the Unicode syntax from the spec, make the output deterministic, and end every statement with `✨`. The program must run with exit code 0 and print something.
3. Add an exact-output test to `tests/test_example_outputs.py` (create the file if it does not exist). Run the example with `sloperator.runner.run_source`, then assert the complete stdout, an empty stderr, and exit code 0. Cover each distinct output the example claims to demonstrate.
4. Run `uv run ruff format`, then invoke the `validate` skill: `uv run pytest`, `uv run ruff format --check`, `uv run ruff check`, and `uv run ty check`.

A test case should look like:

```python
from pathlib import Path

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_string_addition_exact_output():
    result = run_source((EXAMPLES / "string_addition.slop").read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "slop\ncafé✨\n"
```

Report the files created or updated and the validation results.
