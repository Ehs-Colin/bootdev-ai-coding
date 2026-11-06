---
name: create-and-validate
description: Create a SlopLang feature example and exact-output test, then run the full validation suite
---

# Create and Validate

Use this when a SlopLang language feature needs an example program, an exact-output test, and validation.

1. Load the `create-test-program` skill with the `skill` tool (`id: "create-test-program"`) and follow its workflow. It defines how to read `docs/spec.md`, write the example in `examples/`, and add the exact-output test in `tests/test_example_outputs.py`.
2. Load the `validate` skill with the `skill` tool (`id: "validate"`) and follow its workflow to run the full validation suite.

Use those skills as the source of truth instead of duplicating their instructions. Report the files created or updated and the validation results.
