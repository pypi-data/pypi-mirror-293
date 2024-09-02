from pplox.parser import Parser 
from pplox.scanner import Scanner
from pplox.interpreter import Interpreter, to_string
from pplox.interpreter_error import InterpreterError
import pytest

def evaluate(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    return to_string(Interpreter().evaluate(parser.parse()))

def test_true_false_nil():
    assert evaluate('true') == "true"
    assert evaluate('false') == "false"
    assert evaluate('nil') == "nil"

def test_string():
    assert evaluate('"hello world"') == "hello world"

def test_numbers():
    assert evaluate("10") == "10"
    assert evaluate("9.480") == "9.48"
    assert evaluate("2.30") == "2.3"

def test_grouping():
    assert evaluate('("hello world!")') == 'hello world!'
    assert evaluate("(true)") == "true"
    assert evaluate("((false))") == "false"
    assert evaluate("(123.40)") == "123.4"

def test_truthy():
    assert evaluate("-73") == "-73"
    assert evaluate("!true") == "false"
    assert evaluate("!10.40") == "false"
    assert evaluate("!((false))") == "true"

def test_multiplication_division():
    assert evaluate("8 * 8") == "64"
    assert evaluate("80 / 10") == "8" 

def test_minus_plus():
    assert evaluate("20 + 74 - (-(14 - 33))") == "75"

def test_concat():
    assert evaluate('"Hello" + " world"') == "Hello world"
    assert evaluate('"42" + "42"') == "4242"

def test_greater_less():
    assert evaluate("123 >= 123") == "true"
    assert evaluate("124 > 123") == "true"
    assert evaluate("12837 < 1283") == "false"
    assert evaluate("321 <= 321") == "true"

def test_equality():
    assert evaluate('"foo" != "bar"') == "true"
    assert evaluate('"hello" == "world"') == "false"
    assert evaluate('"foo" == "foo"') == "true"

def test_negation_error_handling():
    with pytest.raises(InterpreterError):
        evaluate('-"foo"')
    with pytest.raises(InterpreterError):
        evaluate('-("foo" + "bar")')
    with pytest.raises(InterpreterError):
        evaluate('-true')

def test_operand_type_error():
    with pytest.raises(InterpreterError):
        evaluate('"foo" * 42')
    with pytest.raises(InterpreterError):
        evaluate("true / 2")
    with pytest.raises(InterpreterError):
        evaluate('("foo" * "bar")')

def test_plus_type_error():
    with pytest.raises(InterpreterError):
        evaluate('"foo" + true')
    with pytest.raises(InterpreterError):
        evaluate('42 - true')
    with pytest.raises(InterpreterError):
        evaluate('true + false')

def test_relational_type_error():
    with pytest.raises(InterpreterError):
        evaluate('"foo" < false')
    with pytest.raises(InterpreterError):
        evaluate('("foo" + "bar") < 42')
    with pytest.raises(InterpreterError):
        evaluate('false > true')
