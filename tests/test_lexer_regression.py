import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


# A backslash immediately before a raw newline bypasses the unterminated-string
# check in scanner.string(), so the newline is consumed as the escape character.
# These tests pin the resulting diagnostic so a regression there is visible.
@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ("“abc\\\n”", 1, "unknown escape sequence '\\\n'"),
        ("“abc\\\r\n”", 1, "unknown escape sequence '\\\r'"),
    ],
)
def test_backslash_before_raw_newline_is_a_lexical_error(
    source: str, line: int, message: str
):
    with pytest.raises(LexicalError) as info:
        tokenize(source)
    assert info.value.line == line
    assert info.value.message == message
    assert str(info.value) == f"SlopLang lexical error at line {line}: {message}"
