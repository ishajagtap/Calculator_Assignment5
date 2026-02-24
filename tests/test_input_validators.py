# tests/test_input_validators.py
import pytest
from app.input_validators import parse_command
from app.exceptions import InvalidInputError

def test_parse_valid():
    cmd, a, b = parse_command("add 2 3")
    assert cmd == "add"
    assert a == 2.0 and b == 3.0

def test_parse_short_command():
    cmd, a, b = parse_command("undo")
    assert cmd == "undo" and a is None and b is None

def test_parse_invalid_format():
    with pytest.raises(InvalidInputError):
        parse_command("add 2")