"""Tests for autoseachlib.core module."""

import pytest
from autoseachlib.core import hello_world, add_strings


class TestHelloWorld:
    """Tests for the hello_world function."""

    def test_returns_greeting(self):
        result = hello_world()
        assert result == "Hello World from AutoSeachLib!"

    def test_prints_greeting(self, capsys):
        hello_world()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Hello World from AutoSeachLib!"


class TestAddStrings:
    """Tests for the add_strings function."""

    def test_concatenates_two_strings(self):
        result = add_strings("Hello, ", "World!")
        assert result == "Hello, World!"

    def test_empty_strings(self):
        result = add_strings("", "")
        assert result == ""

    def test_one_empty_string(self):
        assert add_strings("hello", "") == "hello"
        assert add_strings("", "world") == "world"

    def test_raises_on_non_string_first_arg(self):
        with pytest.raises(TypeError, match="Expected str for argument 'a'"):
            add_strings(123, "world")

    def test_raises_on_non_string_second_arg(self):
        with pytest.raises(TypeError, match="Expected str for argument 'b'"):
            add_strings("hello", 456)

    def test_unicode_strings(self):
        result = add_strings("こんにちは", "世界")
        assert result == "こんにちは世界"
