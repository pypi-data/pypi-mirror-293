from pplox.parser import Parser 
from pplox.scanner import Scanner
from pplox.interpreter import Interpreter, to_string

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

