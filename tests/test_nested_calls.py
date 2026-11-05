from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_call_as_argument_to_another_call():
    source = """clanker double(n) {
    ship n * 2✨
}
clanker increment(n) {
    ship n + 1✨
}
hallucinate(double(increment(3)))✨"""
    assert run(source) == "8\n"
