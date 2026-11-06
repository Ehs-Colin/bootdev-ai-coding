from sloperator.runner import run_source


def test_ralph_does_not_run_the_body_when_the_condition_is_false():
    result = run_source(
        """ralph ❌ {
    hallucinate(“never”)✨
}"""
    )

    assert result.stdout == ""
