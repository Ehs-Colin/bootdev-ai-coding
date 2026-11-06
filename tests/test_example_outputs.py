from pathlib import Path

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_equality_exact_output():
    result = run_source((EXAMPLES / "equality.slop").read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "✅\n❌\n❌\n"


def test_short_circuit_exact_output():
    result = run_source((EXAMPLES / "short-circuit.slop").read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "❌\n✅\n"
