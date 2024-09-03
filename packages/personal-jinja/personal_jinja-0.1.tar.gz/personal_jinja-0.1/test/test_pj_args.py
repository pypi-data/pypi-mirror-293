from contextlib import contextmanager
from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path
import pytest  # noqa
from typing import (
    Any,
    Iterator,
    Optional,
    Protocol,
    Sequence,
)
from unittest.mock import Mock, patch

from personal_jinja.__main__ import (
    Config,
    _OpenFile,
    _get_stdin,
    _get_stdout
)


class FileCheck(Protocol):
    def check(self, _open: _OpenFile) -> None: ...


@dataclass
class Std:
    _open: _OpenFile

    def check(self, _open: _OpenFile) -> None:
        assert self._open is _open


Stdin = Std(_get_stdin)
Stdout = Std(_get_stdout)


@dataclass
class Named:
    name: str

    def check(self, _open: _OpenFile) -> None:
        assert hasattr(_open, "__self__")
        assert self.name == str(_open.__self__)


def check_config(
    args: Sequence[str],
    exp_source: FileCheck,
    exp_output: FileCheck,
    exp_backup: Optional[Path],
    **exp_variables: Any
) -> None:
    config = Config.from_args(args)
    exp_source.check(config._open_source)
    exp_output.check(config._open_output)
    assert exp_backup == config.backup
    assert exp_variables == config.variables


def test_no_arg():
    check_config(
        [],
        Stdin,
        Stdout,
        None,
    )


@contextmanager
def setting_time(ts: float = 1725229823.0) -> Iterator[Mock]:
    with patch("personal_jinja.__main__.time.time", return_value=1725229823.0) as mock:
        yield mock


@pytest.mark.parametrize(
    "args",
    [["-f", "asdf.md"], ["--file", "asdf.md"], ["--file=asdf.md"]]
)
def test_named_file(args):
    with setting_time():
        check_config(
            args,
            Named("asdf.md"),
            Named("asdf.md"),
            Path("asdf.md.2024-09-01_18.30.23")
        )


@pytest.mark.parametrize(
    "args",
    [["-f", "input.md", "-o", "out.md"], ["--output=out.md", "--file=input.md"]]
)
def test_named_other_output(args):
    check_config(
        args,
        Named("input.md"),
        Named("out.md"),
        None
    )


def test_just_named_output():
    check_config(
        ["--output", "out.md"],
        Stdin,
        Named("out.md"),
        None
    )


def test_output_stdout():
    check_config(
        ["-o", "-", "-f", "asdf.md"],
        Named("asdf.md"),
        Stdout,
        None
    )


@pytest.mark.parametrize(
    "args",
    [
        ["-f", "note.md", "-r"],
        ["--reverse", "--file=note.md"]
    ]
)
def test_reverse(args):
    with setting_time():
        check_config(
            args,
            Named("note.md"),
            Named("note.md.2024-09-01_18.30.23"),
            None
        )


@pytest.mark.parametrize(
    "args,expected_output",
    [
        [["-f", "note.md", "-r", "-o", "-"], Stdout],
        [["-ro", "out.md", "--file=note.md"], Named("out.md")],
    ]
)
def test_reverse_cancelled_by_output(args, expected_output):
    check_config(
        args,
        Named("note.md"),
        expected_output,
        None
    )


@pytest.mark.parametrize(
    "args,expected_output",
    [
        (["--reverse"], Stdout),
        (["-ro", "out.md"], Named("out.md")),
    ]
)
def test_reverse_ignored_on_stdin_source(args, expected_output):
    check_config(
        args,
        Stdin,
        expected_output,
        None
    )


@pytest.mark.parametrize(
    "arg,ext",
    [
        (".asdf", ".asdf"),
        (".%m-%d", ".09-01")
    ]
)
def test_change_extension(arg, ext):
    with setting_time():
        check_config(
            ["-f", "note.md", "-x", arg],
            Named("note.md"),
            Named("note.md"),
            Path("note.md" + ext)
        )


def test_variables():
    check_config(
        [
            'a=null',
            'b=8',
            'cd=5.6',
            'e="asdf"',
            'fg=[4, 8, 67]',
            'hij={"asdf": "qwer", "zxcv": "poiu"}',
            "xy_z=true",
            "uv=false",
        ],
        Stdin,
        Stdout,
        None,
        a=None,
        b=8,
        cd=5.6,
        e="asdf",
        fg=[4, 8, 67],
        hij={"asdf": "qwer", "zxcv": "poiu"},
        xy_z=True,
        uv=False
    )


def test_illegal_definition():
    with pytest.raises(ValueError):
        Config.from_args(['asdf qwerty'])


@pytest.mark.parametrize("name", ["1asdf", "qwer-zxcv", "hey!"])
def test_illegal_variable_name(name):
    with pytest.raises(ValueError):
        Config.from_args([f'{name}=8'])


def test_malformed_json_value():
    with pytest.raises(JSONDecodeError):
        Config.from_args(['asdf={"zxcv": [5, 6}'])


@pytest.mark.parametrize(
    "args,expected_backup",
    [
        (["-f", "note.md"], Path("note.md.2024-09-01_18.30.23")),
        (["-nf", "note.md"], None),
    ]
)
def test_no_backup(args, expected_backup):
    with setting_time():
        check_config(args, Named("note.md"), Named("note.md"), expected_backup)
