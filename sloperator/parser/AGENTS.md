# AGENTS.md — parser

Conventions for `sloperator/parser/`. See the root `AGENTS.md` for repo-wide setup and the pipeline overview, and `docs/spec.md` for the grammar.

## One method per grammar rule

Give every grammar rule its own `Parser` method, named after the rule it implements (`declaration`, `statement`, `if_stmt`, `logic_or`, `comparison`, `primary`, and so on). Keep the recursive-descent structure readable: a rule's method calls the methods for the rules it references rather than inlining their logic.

- Put precedence levels in separate methods, one per level, chaining downward (`expression` -> `logic_or` -> `logic_and` -> `comparison` -> ... -> `primary`).
- Reusable helpers that are not grammar rules (`expect`, `match`, `check`, `advance`, `error`, `terminator`) stay separate and are not named after rules. A helper that handles a rule's trailing loop (`factor_tail`) is acceptable, but prefer a single method when the rule is simple.
- Add a method when you add a rule; do not grow an existing rule's method to cover two rules.

## Syntax errors describe the token that was found

Every syntax error must say what the parser actually found, not just what it wanted. Route diagnostics through `Parser.error` so they follow the standard shape:

- Mid-input: `"<expectation>, found '<lexeme>'"`.
- At end of input: `"<expectation>, but reached end of file"` (no lexeme, since there is none).

Pass an expectation as the message to `expect`/`terminator`/`error` (for example `"expected ')' after parameters"`); let `error` append the found token. Do not construct `SlopSyntaxError` messages that omit the found token, and do not duplicate the `, found ...` suffix yourself.

Context errors that do not go through `error` (a duplicate parameter name, `ship` outside a `clanker`, a nested `clanker`) must still identify the offending token or name, as the existing messages do.

Tests assert exact messages and line numbers, so when a diagnostic changes, update the matching tests in `tests/` in the same change.
