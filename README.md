# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Quick Start

```bash
uv run sloperator.py path/to/program.slop          # run a program
uv run sloperator.py --check path/to/program.slop # check syntax only
```

## Validation

```bash
uv run pytest               # tests
uv run ruff format --check  # formatting
uv run ruff check           # linting
uv run ty check             # type checking
```

## Example

```slop
— Comments start with an em dash. Statements end with sparkles.
clanker describe(count) {
    vibe count > 1 {
        ship “big slop”✨
    } nah {
        ship “small slop”✨
    }
}

loadbearing MAX = 3✨
slop count = 0✨

ralph count < MAX {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

Prints `small slop` twice, then `big slop`. See [docs/spec.md](docs/spec.md) for the complete language specification.

**Layout:** `sloperator.py` is the CLI; `sloperator/` holds the `lexer/`, `parser/`, and `evaluator/` stages; `tests/` is the pytest suite; `examples/` has sample programs.

## Playground

Run `uv run playground/server.py`, then open <http://localhost:8080>.
