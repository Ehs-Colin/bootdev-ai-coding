from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def test_equality_binds_looser_than_comparison():
    (statement,) = parse(tokenize("1 < 2 == ✅✨"))
    assert isinstance(statement, ExprStmt)

    expr = statement.expression
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.LESS
    assert isinstance(expr.right, Literal) and expr.right.value is True

    result = run_source("hallucinate(1 < 2 == ✅)✨")
    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0
