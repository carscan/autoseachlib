"""Tests for autoseachlib.cli module."""

from autoseachlib.cli import main


class TestCli:
    """Tests for the CLI entry point."""

    def test_hello_command(self, capsys):
        exit_code = main(["hello"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Hello World from AutoSeachLib chander!" in captured.out

    def test_add_command(self, capsys):
        exit_code = main(["add", "Hello, ", "World!"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Hello, World!" in captured.out

    def test_no_command_shows_help(self, capsys):
        exit_code = main([])
        assert exit_code == 1

    def test_version_flag(self, capsys):
        try:
            main(["--version"])
        except SystemExit as e:
            assert e.code == 0
        captured = capsys.readouterr()
        assert "autoseachlib" in captured.out
