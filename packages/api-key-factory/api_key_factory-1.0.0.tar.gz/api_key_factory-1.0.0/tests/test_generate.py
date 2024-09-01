# -*- coding: utf-8 -*-

from click.testing import CliRunner

from api_key_factory import api_key_factory


class Test_generate:
    def test_generate_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(api_key_factory.cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "generate [OPTIONS]" in result.stdout

    def test_generate_without_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(api_key_factory.cli, ["generate"])
        assert result.exit_code == 0
        out = result.stdout
        lines = out.splitlines()
        assert len(lines) == 1
        key_hash = lines[0].split()
        assert len(key_hash[0]) == 36
        assert len(key_hash[1]) == 64

    def test_generate_with_n_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(api_key_factory.cli, ["generate", "-n", "3"])
        assert result.exit_code == 0
        out = result.stdout
        lines = out.splitlines()
        assert len(lines) == 3
        key_hash = lines[0].split()
        assert len(key_hash[0]) == 36
        assert len(key_hash[1]) == 64

    def test_generate_with_num_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(api_key_factory.cli, ["generate", "--num", "3"])
        assert result.exit_code == 0
        out = result.stdout
        lines = out.splitlines()
        assert len(lines) == 3
        key_hash = lines[0].split()
        assert len(key_hash[0]) == 36
        assert len(key_hash[1]) == 64
